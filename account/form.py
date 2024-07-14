from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ShopUser


class ShopUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ('phone', 'address', 'first_name', 'last_name', 'is_active', 'is_superuser', 'date_joined')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('already exited')
            else:
                if ShopUser.objects.filter(phone=phone).exists():
                    raise forms.ValidationError('already exited')
        if ShopUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError('already exited')
        if not phone.isdigit():
            raise forms.ValidationError('phone must be started with 09')
        if len(phone) != 11:
            raise forms.ValidationError('phone must have 11 digits')
        return phone


class ShopUserChangeForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ('phone', 'address', 'first_name', 'last_name', 'is_active', 'is_superuser', 'date_joined')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('already exited')
            else:
                if ShopUser.objects.filter(phone=phone).exists():
                    raise forms.ValidationError('already exited')
        if ShopUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError('already exited')
        if not phone.isdigit():
            raise forms.ValidationError('phone must be started with 09')
        if len(phone) != 11:
            raise forms.ValidationError('phone must have 11 digits')
        return phone
