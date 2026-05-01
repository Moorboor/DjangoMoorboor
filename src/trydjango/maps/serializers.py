from rest_framework import serializers
from .models import Product
from django.urls import reverse

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["category", "title", "image_url", "description", "date", "geocoor", "url"]
        
    def get_image_url(self, product):
        return product.image_file.url
    
    def get_url(self, product):
        request = self.context.get("request")
        path = reverse("artworkDetail", kwargs={"pk": product.pk})
        return request.build_absolute_uri(path) if request else path