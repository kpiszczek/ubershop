from django.forms import ModelForm
# from django.db import models

from auction.models import AuctionItem
#from base.forms import BaseForm

class AuctionForm(ModelForm):
    class Meta:
        model = AuctionItem
        exclude = ('created_at','close_date','bids',
                   'payment_date','created_by')