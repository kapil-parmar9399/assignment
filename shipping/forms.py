from django import forms
from django.core.exceptions import ValidationError

from .models import Product


class OrderRequestForm(forms.Form):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        help_text="Select all products in the order.",
    )
    quantity = forms.IntegerField(min_value=1, max_value=100, initial=1, help_text="This quantity applies to each selected product.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["products"].queryset = Product.objects.order_by("name")

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("products"):
            raise ValidationError("Choose at least one product to create an order.")
        return cleaned
