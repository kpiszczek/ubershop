from django import forms
from core.models import ShopUser

class RegisterForm(forms.Form):
    class Meta:
        model = ShopUser
        fields = ('username','password', 'first_name','last_name', 'email', 'organisation', 'address', 'tax_id')