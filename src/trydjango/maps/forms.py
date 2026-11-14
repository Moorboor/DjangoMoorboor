# forms.py
from django import forms
from .models import ProductMedia


class ProductMediaForm(forms.ModelForm):  

    class Meta:
        model = ProductMedia
        fields = [
            "media_type",  
            "image",       
            "video",       
            "caption",
            "order",
        ]