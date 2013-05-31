from django import forms

from ordermanager.models import ShipmentMethod

class OrderForm(forms.Form):
    shipment_method = forms.ModelChoiceField(queryset=ShipmentMethod.objects.all())
    details = forms.CharField(widget=forms.Textarea)