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
            cart.clear()
            return redirect('shop:products_list')

    else:
        form = OrderCreateForm()
    return render(request, 'order/order_create.html', {'form': form, 'cart': cart})
