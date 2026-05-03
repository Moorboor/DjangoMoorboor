from django.contrib import admin
from django.utils.html import format_html  # ✅ imported

from .models import Product, Person, ProductPerson, ProductMedia


class ProductMediaInline(admin.TabularInline):  # ✅ renamed to match what it is
    model = ProductMedia                         # ✅ correct model
    extra = 1
    fields = ["media_type", "image", "video", "caption", "order", "preview"]
    readonly_fields = ["preview"]

    def preview(self, obj):
        if obj.media_type == "image" and obj.image:
            return format_html('<img src="{}" style="height:60px; border-radius:4px;">', obj.image.url)
        if obj.media_type == "video" and obj.video:
            return format_html('<video src="{}" style="height:60px;" controls></video>', obj.video.url)
        return "—"
    preview.short_description = "Preview"


@admin.register(Product)                        # ✅ replaces plain admin.site.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductMediaInline]              # ✅ carousel media lives inside the product page


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductPerson)
class ProductPersonAdmin(admin.ModelAdmin):
    list_display = ["product", "person", "roles", "order"]
    list_filter = ["roles"]
    search_fields = ["product__title", "person__name"]


@admin.register(ProductMedia)                   
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ["product", "media_type", "preview", "caption", "order"]
    list_filter = ["media_type", "product"]
    search_fields = ["product__title", "caption"] 
    ordering = ["product", "order"]

    def preview(self, obj):
        if obj.media_type == "image" and obj.image:
            return format_html('<img src="{}" style="height:50px; border-radius:4px;">', obj.image.url)
        if obj.media_type == "video" and obj.video:
            return format_html('<video src="{}" style="height:50px;" controls></video>', obj.video.url)
        return "—"
    preview.short_description = "Preview"