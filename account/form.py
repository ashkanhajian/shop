from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ShopUser


class ShopUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ('phone', 'address', 'first_name', 'last_name', 'is_active', 'is_superuser', 'date_joined')


class ShopUserChangeForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ('phone', 'address', 'first_name', 'last_name', 'is_active', 'is_superuser', 'date_joined')
