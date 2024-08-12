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
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
import requests
import json


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
            # cart.clear()
            return redirect('orders:request')

    else:
        form = OrderCreateForm()
    return render(request, 'order/order_create.html', {'form': form, 'cart': cart})




# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


CallbackURL = 'http://127.0.0.1:7000/verify/'


def send_request(request):
    cart = Cart(request)
    description = ''
    for item in cart:
        description += str(item['product'].name)
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": cart.get_final_price(),
        "Description": description,
        "Phone": request.user.phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response_json = response.json()
            authority = response_json['Authority']
            if response_json['Status'] == 100:
                return redirect(ZP_API_STARTPAY + authority)
            else:
                return HttpResponse('Error')
        return HttpResponse('response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')


def verify(authority):
    data = {
        "MerchantID": settings.MERCHANT,
        #"Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            reference_id = response_json['RefID']
            if response['Status'] == 100:
                return HttpResponse(f'successful , RefID: {reference_id}')

            else:
                return HttpResponse('Error')
        return HttpResponse('response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')
