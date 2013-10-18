from django import forms

from base.models import BaseItem


class SearchForm(forms.Form):
    phrase = forms.CharField()


class BaseForm(forms.ModelForm):

    class Meta:
        model = BaseItem
