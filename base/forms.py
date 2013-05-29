from django.forms import ModelForm

from base.models import BaseItem

class BaseForm(ModelForm):
    class Meta:
        model = BaseItem