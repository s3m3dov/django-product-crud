from django import forms

from apps.product.models import Product
from config.validators import validate_file_size


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ["uuid", "created", "updated", "logo", "rotate_duration"]

    logo_file = forms.FileField(required=True, validators=[validate_file_size])
