from django.db import models
from django.core.exceptions import ValidationError
import os


class Person(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    image_file = models.ImageField(upload_to="people/", null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    method_choices = {
        "Water colors": "Water colors",
        "Wax Crayons": "Wax Crayons",
        "Color pencils": "Color pencils",
        "Guache": "Guache",
        "Mixed": "Mixed",
        "Fine liner": "Fine liner",
        "Crayons": "Crayons",
        "Ink": "Ink",
    }

    category_choices = {
        "Landscapes": "Landscapes",
        "Architecture": "Architecture",
        "People": "People",
        "Animals": "Animals",
        "Objects": "Objects",
    }
    
    title = models.CharField(max_length=100)
    image_file = models.ImageField(upload_to="arts/")
    description = models.TextField(null=True)
    date = models.DateField(default="2025-11-16")
    method = models.CharField(choices=method_choices, default="Water colors")
    aspect_ratio = models.CharField(choices={"2:1": "2:1", "1:1": "1:1", "1:2": "1:2"})
    category = models.CharField(choices=category_choices, default="Landscapes")
    geocoor = models.CharField(max_length=100, default="80.00, 80.00", blank=True)
    visit_count = models.PositiveIntegerField(default=0)  # Denormalized count for performance

    artist = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="created_products",
    )
    people = models.ManyToManyField(
        Person,
        through="ProductPerson",
        related_name="products",
        blank=True,
    )

    def __str__(self):
        return self.title


class ProductVisit(models.Model):
    """Track unique session visits to products"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name="visits"
    )
    session_key = models.CharField(max_length=40)
    visited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'session_key')
        verbose_name = "Product Visit"
        verbose_name_plural = "Product Visits"

    def __str__(self):
        return f"{self.product.title} — Session: {self.session_key[:10]}..."


class ProductPerson(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    roles = models.CharField(
        max_length=30,
        choices=[
            ("subject", "Subject / depicted"),
            ("other", "Other"),
        ],
        default="subject",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:                                  
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "person", "roles"],  
                name="unique_person_role_per_product",
            )
        ]

    def __str__(self):
        return f"{self.person} — {self.product} ({self.roles})"


def validate_video_file(value):
    allowed_extensions = [".mp4", ".webm", ".ogg", ".mov"]
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(
            f"Unsupported video format. Allowed: {', '.join(allowed_extensions)}"
        )


class ProductMedia(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image", "Image"
        VIDEO = "video", "Video"

    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="carousel_images"
    )
    media_type = models.CharField(
        max_length=10,
        choices=MediaType.choices,
        default=MediaType.IMAGE,
    )
    image = models.ImageField(upload_to="products/carousel/images/", blank=True)
    video = models.FileField(
        upload_to="products/carousel/videos/",
        blank=True,
        validators=[validate_video_file],
    )
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def clean(self):
        if self.media_type == self.MediaType.IMAGE and not self.image:
            raise ValidationError({"image": "An image file is required."})
        if self.media_type == self.MediaType.VIDEO and not self.video:
            raise ValidationError({"video": "A video file is required."})

    def __str__(self):
        return f"{self.product} — {self.get_media_type_display()} ({self.order})"