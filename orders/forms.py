from django import forms
from account.models import ShopUser
from .models import Order


class PhoneVerificationFrom(forms.Form):
    phone = forms.CharField(max_length=11, label='phone')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if ShopUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError('phone already exits!')
        return phone


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'city', 'address', 'postal_code', 'province']
