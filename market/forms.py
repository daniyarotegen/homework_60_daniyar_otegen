from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator, MinValueValidator
from market.models import Product


class CustomMaxValidator(BaseValidator):
    def __init__(self, limit_value=50):
        message = 'Maximum description length is %(limit_value)s symbols. You entered %(show_value)s symbols'
        super().__init__(limit_value=limit_value, message=message)

    def compare(self, value, limit_value):
        return limit_value < value

    def clean(self, x):
        return len(x)


class CustomMinValidator(BaseValidator):
    def __init__(self, limit_value=2):
        message = 'Minimum description length is %(limit_value)s symbols. You entered %(show_value)s symbols'
        super().__init__(limit_value=limit_value, message=message)

    def compare(self, value, limit_value):
        return limit_value > value

    def clean(self, x):
        return len(x)


class ProductForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='Description',
        validators=(CustomMaxValidator(), CustomMinValidator()))

    quantity = forms.IntegerField(
        validators=(MinValueValidator(0),),
        required=True,
        label='Quantity')

    price = forms.IntegerField(
        validators=(MinValueValidator(0),),
        required=True,
        label='Price')

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'quantity', 'price']
        labels = {
            'name': 'Name',
            'description': 'Description',
            'image': 'Image',
            'category': 'Category',
            'quantity': 'Quantity',
            'price': 'Price'
        }


class ProductSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search by name')
