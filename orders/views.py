from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from account.models import ShopUser
import random
from card.views import add_to_cart
from django.contrib.auth import login


# Create your views here.

def verify_phone(request):
    if request.method == 'POST':
        form = PhoneVerificationFrom(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            token = {'token': ''.join(random.choices('0123456789', k=6))}
            request.session['verification_code'] = token['token']
            request.phone = phone
            print('tokens')
            # send_sms_with_template(phone, token, 'verify')
            messages.error(request, 'verification code sent successfully')
            return redirect('order/verify')
    else:
        form = PhoneVerificationFrom()
    return render(request, 'order_forms/verify_phone.html', {'form': form})
def verify_code(request):
    pass