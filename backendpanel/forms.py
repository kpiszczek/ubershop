from django import forms
from django.forms.formsets import formset_factory

from base.models import BaseItem
from core.models import Category
from core.models import ShipmentMethod
from eshop.models import EShopItem
from groupbuy.models import GroupOffer


class EshopItemForm(froms.Form):
    name = forms.CharField()
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    description = forms.TextField()
    thumb = forms.ImageField()
