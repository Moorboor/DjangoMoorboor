from django.db import models
from django.core.exceptions import ValidationError
import os
from django.utils import timezone


class Person(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    image_file = models.ImageField(upload_to="people/", null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    REGION_CHOICES = [
        ('Svalbard', 'Svalbard'),
        ('Central America', 'Central America'),
        ('Uzbekistan', 'Uzbekistan'),
    ]
    
    CATEGORY_CHOICES = [
        ('Landscapes', 'Landscapes'),
        ('Architecture', 'Architecture'),
        ('People', 'People'),
        ('Animals', 'Animals'),
        ('Objects', 'Objects'),
    ]
    
    METHOD_CHOICES = [
        ('Water colors', 'Water colors'),
        ('Wax Crayons', 'Wax Crayons'),
        ('Color pencils', 'Color pencils'),
        ('Guache', 'Guache'),
        ('Mixed', 'Mixed'),
        ('Fine liner', 'Fine liner'),
        ('Crayons', 'Crayons'),
        ('Ink', 'Ink'),
    ]
    
    ASPECT_RATIO_CHOICES = [
        ('2:1', '2:1'),
        ('1:1', '1:1'),
        ('1:2', '1:2'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    # Image & Display
    image_file = models.ImageField(upload_to="arts/")
    aspect_ratio = models.CharField(
        max_length=10,
        choices=ASPECT_RATIO_CHOICES,
        default='1:1'
    )
    
    # Classification
    region = models.CharField(
        max_length=50,
        choices=REGION_CHOICES,
        help_text="Geographic region (Svalbard, Central America, Uzbekistan)",
        default="Central America"
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Landscapes',
        help_text="Subject category (Landscapes, Architecture, etc.)"
    )
    method = models.CharField(
        max_length=50,
        choices=METHOD_CHOICES,
        default='Water colors',
        help_text="Artistic method used"
    )
    
    # Metadata
    date = models.DateField(default='2025-11-16')
    geocoor = models.CharField(
        max_length=100,
        default='80.00, 80.00',
        blank=True,
        help_text="Geographic coordinates"
    )
    visit_count = models.PositiveIntegerField(default=0)
    
    # Relations
    artist = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name='created_products',
    )
    people = models.ManyToManyField(
        Person,
        through='ProductPerson',
        related_name='products',
        blank=True,
    )
    
    def __str__(self):
        return f"{self.title} ({self.region})"
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Products'

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
    
    

class Comment(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"Comment by {self.name} on {self.product.title}"