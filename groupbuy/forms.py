from django.forms import ModelForm
from groupbuy.models import GroupOffer

class GroupOfferForm(forms.Form):
    base = models.OneToOneField(BaseForm)
    class Meta:
        model = GroupOffer
        exclute = ('created_at','buyers','current_num_buyers')