from django.forms import ModelForm
from eshop.models import EShopItem

class EShopItemForm(ModelForm):
    class Meta:
        model = EShopItem
        exclude = ('created_at',)