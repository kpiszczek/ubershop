from django.forms import ModelForm
from auction.models import AuctionItem

class AuctionForm(forms.Form):
    base = models.OneToOneField(BaseForm)
    class Meta:
        model = AuctionItem
        exclude = ('created_at','close_date','bids',
                   'payment_date','created_by')