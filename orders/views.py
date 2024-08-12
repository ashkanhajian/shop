from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import OrderItem
from card.cart import Cart
from account.models import ShopUser
import random
from card.views import add_to_cart
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


# Create your views here.

def verify_phone(request):
    if request.user.is_authenticated:
        return redirect('orders:create_order')
    if request.method == 'POST':
        form = PhoneVerificationFrom(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            token = {'token': ''.join(random.choices('0123456789', k=6))}
            request.session['verification_code'] = token['token']
            request.session['phone'] = phone
            print(token)
            # send_sms_with_template(phone, token, 'verify')
            messages.error(request, 'verification code sent successfully')
            return redirect('orders:verify_code')
    else:
        form = PhoneVerificationFrom()
    return render(request, 'order_forms/verify_phone.html', {'form': form})


def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            verification_code = request.session['verification_code']
            phone = request.session['phone']
            if code == verification_code:
                user = ShopUser.objects.create_user(phone=phone)
                user.set_password(''.join((random.choices('123456789', k=16))))
                # send sms
                print(user.password)
                login(request, user)
                del request.session['verification_code']
                del request.session['phone']
                return redirect('orders:create_order')
            else:
                messages.error(request, 'Verification code is incorrect')
    return render(request, 'order/verify_code.html')


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.buyer = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity']
                                         , weight=item['weight'])
            #cart.clear()
            return redirect('shop:products_list')

    else:
        form = OrderCreateForm()
    return render(request, 'order/order_create.html', {'form': form, 'cart': cart})


from django.conf import settings
import requests
import json

# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:7000/verify/'


def send_request(request):
    cart = Cart(request)
    description = ''
    for item in cart:
        description += str(item.product.name)
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": cart.get_final_price(),
        "Description": description,
        "Phone": request.user.phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                cart.clear()
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                        'authority': response['Authority']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


def verify(authority):
    data = {
        "MerchantID": settings.MERCHANT,
        #"Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return response