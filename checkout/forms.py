from django import forms
from .models import Order

class MakePaymentForm(forms.Form):

    MONTH_CHOICES = [(i, i,) for i in range(1, 13)]
    YEAR_CHOICES = [(i, i,) for i in range(2015, 2036)]

    credit_card_number = forms.CharField(label='Numero de tarjeta', required=False)
    cvv = forms.CharField(label='Codigo de seguridad (CVV)', required=False)
    expiry_month = forms.ChoiceField(label="Mes", choices=MONTH_CHOICES, required=False)
    expiry_year = forms.ChoiceField(label="anno", choices=YEAR_CHOICES, required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)
    
    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'phone_number', 'country', 'postcode', 'town_or_city', 'street_address_1', 'street_address_2', 'county')