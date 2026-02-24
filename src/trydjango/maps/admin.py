from django.contrib import admin

from .models import Product, Person, ProductPerson, ProductImage
# Register your models here.

admin.site.register(Product)
admin.site.register(Person)
admin.site.register(ProductPerson)
admin.site.register(ProductImage)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]