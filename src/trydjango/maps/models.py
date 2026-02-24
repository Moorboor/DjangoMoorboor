from django.db import models
    
class Person(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    image_file = models.ImageField(upload_to=f"people/", null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    country_choices = {
        "Germany": "Germany",
        "Svalbard": "Svalbard", 
        "Costa Rica": "Costa Rica",
        "Nicaragua": "Nicaragua",
        "Honduras": "Honduras",
        "Guatemala": "Guatemala",
        "Uzbekistan": "Uzbekistan",
        "Vietnam": "Vietnam",
        "Portugal": "Portugal"
        }
    
    method_choices = {
        "Water colors": "Water colors",
        "Wax Crayons": "Wax Crayons",
        "Color pencils": "Color pencils",
        "Guache": "Guache",
        "Mixed": "Mixed",
        "Fine liner": "Fine liner",
        "Crayons": "Crayons",
        "Ink": "Ink" 
    }
    
    category_choices = {
        "Landscapes": "Landscapes",
        "Architecture": "Architecture",
        "People": "People",
        "Animals": "Animals",
        "Objects": "Objects"
    }
    
    country = models.CharField(choices=country_choices)
    title = models.CharField(max_length=100)
    image_file = models.ImageField(upload_to=f"arts/")
    description = models.TextField(null=True)
    date = models.DateField(default="2025-11-16")
    method = models.CharField(choices=method_choices, default="Water colors")
    aspect_ratio = models.CharField(choices={"2:1": "2:1", "1:1": "1:1", "1:2": "1:2"})
    category = models.CharField(choices=category_choices, default="Landscapes")
    geocoor = models.CharField(max_length=100, default="80.00, 80.00")


    artist = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="created_products",
    )
    people = models.ManyToManyField(
        Person,
        through="ProductPerson",
        related_name="products",
        blank=True
    )
    
class ProductPerson(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    roles = models.CharField(
    max_length=30,
        choices=[
            ("subject", "Subject / depicted"),
            ("other", "Other")
        ],
        default="subject",
    )
    order = models.PositiveIntegerField(default=0)
    
    
class ProductImage(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="carousel_images")
    image = models.ImageField(upload_to="products/carousel/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
    
class Meta:
    ordering = ["order"]
    constraints = [
        models.UniqueConstraint(
            fields=["product", "person", "role"],
            name="unique_person_role_per_product",
        )
    ]