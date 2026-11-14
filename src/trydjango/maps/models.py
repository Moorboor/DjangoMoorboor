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
        ('Europe', 'Europe'),
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

    @property
    def scrolly_steps(self):
        """
        Builds the scrollytelling path where:
        - Step 1 is locked to the Title + Metadata underneath it.
        - Step 2 onwards is dynamically populated by customizable admin entries.
        """
        db_steps = list(self.scrolly_steps_rel.all())

        # Grab first step's positioning rules if customized in admin, else use default framing
        first_step_layout = "bottom-left"
        first_scale, first_x, first_y = 1.0, 0, 0
        if db_steps:
            first_scale = db_steps[0].scale
            first_x = db_steps[0].x
            first_y = db_steps[0].y
            first_layout = db_steps[0].layout

        # LOCK STEP 1: Always Product Title + Metadata
        steps = [{
            "title": self.title,
            "layout": first_step_layout,
            "scale": first_scale,
            "x": first_x,
            "y": first_y,
            "meta_items": [
                {"label": "Location", "value": self.region},
                {"label": "Year", "value": self.date.strftime('%d %B %Y') if self.date else ''},
                {"label": "Medium", "value": self.method},
                {"label": "Category", "value": self.category},
            ]
        }]

        # STEP 2 ONWARDS: Custom configurations from database
        if len(db_steps) > 1:
            for db_step in db_steps[1:]:
                step_data = {
                    "layout": db_step.layout,
                    "scale": db_step.scale,
                    "x": db_step.x,
                    "y": db_step.y,
                }
                if db_step.description:
                    step_data["title"] = db_step.title or "Observations"
                    step_data["description"] = db_step.description
                else:
                    step_data["title"] = db_step.title or "Details"
                steps.append(step_data)
        else:
            # Fallback standard Step 2 path if no custom admin steps exist yet
            if self.description:
                steps.append({
                    "title": "Observations",
                    "description": self.description,
                    "layout": "bottom-right",
                    "scale": 1.8, "x": 12, "y": -8,
                })

        return steps
    
    def __str__(self):
        return f"{self.title} ({self.region})"
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Products'

# This model gets its own separate Meta configuration
class ScrollyStep(models.Model):
    LAYOUT_CHOICES = [
        ('bottom-left', 'Bottom Left'),
        ('top-right', 'Top Right'),
        ('bottom-right', 'Bottom Right'),
        ('top-left', 'Top Left'),
    ]

    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='scrolly_steps_rel'
    )
    order = models.PositiveIntegerField(
        default=0, 
        help_text="Display order sequence (0, 1, 2...)"
    )
    scale = models.FloatField(
        default=1.0, 
        help_text="Zoom factor (e.g. 1.0 = normal, 2.5 = deep detail zoom)"
    )
    x = models.FloatField(
        default=0.0, 
        help_text="Horizontal panning percentage (e.g. -15 moves left, 15 moves right)"
    )
    y = models.FloatField(
        default=0.0, 
        help_text="Vertical panning percentage (e.g. -15 moves up, 15 moves down)"
    )
    layout = models.CharField(
        max_length=20, 
        choices=LAYOUT_CHOICES, 
        default='bottom-left',
        help_text="Where the text floats relative to the drawing negative space"
    )
    title = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        help_text="Optional text header override"
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        help_text="Add text here to display a scrollable description card at this step"
    )

    class Meta:
        ordering = ['order']  # Keeps the steps sorted cleanly inside each product page

    def __str__(self):
        return f"Step {self.order} for {self.product.title}"



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