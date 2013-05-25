from django.forms import ModelForm
from eshop.models import EShopItem

class EShopItemForm(forms.Form):
    base = models.OneToOneField(BaseForm)
    class Meta:
        model = EShopItem
        exclude = ('created_at',)