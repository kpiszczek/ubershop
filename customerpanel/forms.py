from django import forms
from django.forms.formsets import formset_factory

from core.models import ShopUser

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    address = forms.CharField(widget=forms.Textarea)
    organisation = forms.CharField(required=False, widget=forms.Textarea)
    tax_id = forms.CharField(required=False)
    
    
class EditUserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    address = forms.CharField(widget=forms.Textarea)
    organisation = forms.CharField(required=False, widget=forms.Textarea)
    tax_id = forms.CharField(required=False)
    
class CartItemForm(forms.Form):
    quantity = forms.IntegerField()
    
CartFormset = formset_factory(CartItemForm)