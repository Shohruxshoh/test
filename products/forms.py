from django import forms

class PaymentForm(forms.Form):
    card = forms.CharField(max_length=16)