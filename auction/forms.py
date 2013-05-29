from django import forms
# from django.db import models

from auction.models import AuctionItem
#from base.forms import BaseForm
class BidForm(forms.Form):
    bid = forms.DecimalField(max_digits=15,decimal_places=2)
    
class AuctionForm(forms.ModelForm):
    class Meta:
        model = AuctionItem
        exclude = ('created_at','close_date','bids',
                   'payment_date','created_by')
