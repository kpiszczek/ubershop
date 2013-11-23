from django import forms
from django.forms.formsets import formset_factory

from base.models import BaseItem
from core.models import Category
from core.models import ShipmentMethod
from eshop.models import EShopItem
from groupbuy.models import GroupOffer


#class EshopItemForm(forms.Form):
#    name = forms.CharField()
#    category = forms.ModelChoiceField(queryset=Category.objects.all())
#    description = forms.CharField(widget=forms.Textarea)
#    thumb = forms.ImageField()

class CategoryForm(forms.Form):
    name = forms.CharField()

class ShipmentMethodForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(max_digits=15,decimal_places=2)