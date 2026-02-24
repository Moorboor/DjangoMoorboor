from .models import ProductImage

from django import forms


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = [
            "image",
            "caption",
            "order"
        ]
