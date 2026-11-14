from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Person, ProductPerson, ProductMedia, ProductVisit, Comment, ScrollyStep


class ProductMediaInline(admin.TabularInline):  
    model = ProductMedia                        
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
class ScrollyStepInline(admin.TabularInline):
    model = ScrollyStep
    extra = 1  # Shows 1 blank slot ready to add at the bottom
    fields = ('order', 'scale', 'x', 'y', 'layout', 'title', 'description')
    ordering = ('order',)


@admin.register(Product)                       
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'region', 'date')
    inlines = [ProductMediaInline, ScrollyStepInline] 



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
    
@admin.register(ProductVisit)
class ProductVisitAdmin(admin.ModelAdmin):
    list_display = ('product', 'session_key', 'visited_at')
    list_filter = ('product', 'visited_at')
    readonly_fields = ('session_key', 'visited_at', 'product')
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('name', 'content', 'product__title')
    actions = ['approve_comments', 'reject_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"
    
    def reject_comments(self, request, queryset):
        queryset.update(is_approved=False)
    reject_comments.short_description = "Reject selected comments"


