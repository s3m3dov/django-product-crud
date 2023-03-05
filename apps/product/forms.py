from django import forms

from apps.product.models import Product
from config.validators import validate_file_size, validate_file_type


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description"]

    logo_file = forms.FileField(required=True, validators=[validate_file_size, validate_file_type])
