from django import forms
# from django.db import models

from auction.models import AuctionItem
from core.models import Category
#from base.forms import BaseForm

class BidForm(forms.Form):
    bid = forms.DecimalField(max_digits=15,decimal_places=2)
    
class AuctionForm(forms.Form):
    name = forms.CharField()
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    thumb = forms.ImageField()
    image = forms.ImageField()
    start_date = forms.DateTimeField(widget=forms.DateTimeInput)
    planned_close_date = forms.DateTimeField(widget=forms.DateTimeInput)
    start_price = forms.DecimalField(max_digits=15,decimal_places=2)
    reserve_price = forms.DecimalField(max_digits=15,decimal_places=2)
    
class EditAuctionForm(forms.Form):
    name = forms.CharField()
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    properties = forms.CharField(widget=forms.Textarea)
    description = forms.CharField(widget=forms.Textarea)
    thumb = forms.ImageField()
    image = forms.ImageField()
    start_date = forms.DateTimeField(widget=forms.DateTimeInput)
    planned_close_date = forms.DateTimeField(widget=forms.DateTimeInput)
    start_price = forms.DecimalField(max_digits=15,decimal_places=2)
    reserve_price = forms.DecimalField(max_digits=15,decimal_places=2)
