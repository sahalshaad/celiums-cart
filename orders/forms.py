from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line1', 'address_line2', 'city', 'country', 'state', 'order_notes']