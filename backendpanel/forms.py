from django import forms
from django.forms.formsets import formset_factory

from base.models import BaseItem
from core.models import Category
from core.models import ShipmentMethod
from core.models import AvailiabilityStatus
from eshop.models import EShopItem
from groupbuy.models import GroupOffer
from base.models import BaseItem


class EshopItemForm(forms.Form):
    name = forms.CharField()
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    thumb = forms.ImageField(required=False)
    
    image1 = forms.ImageField(required=False)
    image2 = forms.ImageField(required=False)
    image3 = forms.ImageField(required=False)
    
    is_active = forms.BooleanField(widget=forms.CheckboxInput)
    
    properties1 = forms.CharField(required=False)
    properties2 = forms.CharField(required=False)
    properties3 = forms.CharField(required=False)
    properties4 = forms.CharField(required=False)
    properties5 = forms.CharField(required=False)
    properties6 = forms.CharField(required=False)
    pname1 = forms.CharField(required=False)
    pname2 = forms.CharField(required=False)
    pname3 = forms.CharField(required=False)
    pname4 = forms.CharField(required=False)
    pname5 = forms.CharField(required=False)
    pname6 = forms.CharField(required=False)
    
    price = forms.DecimalField(max_digits=15,decimal_places=2)
    is_on_sale = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    discount_price = forms.DecimalField(max_digits=15,decimal_places=2, required=False)
    availiability_status = forms.ModelChoiceField(queryset=AvailiabilityStatus.objects.all().order_by('name'))
    current_stock = forms.IntegerField()
    
class CategoryForm(forms.Form):
    name = forms.CharField()

class ShipmentMethodForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(max_digits=15,decimal_places=2)
    
class GroupOfferForm(forms.Form):
    base = forms.ModelChoiceField(queryset=BaseItem.objects.all().order_by('name'))
    price = forms.DecimalField(max_digits=15,decimal_places=2)
    min_num_buyers = forms.IntegerField()
    availiability_status = forms.ModelChoiceField(queryset=AvailiabilityStatus.objects.all().order_by('name'))
    current_stock = forms.IntegerField()