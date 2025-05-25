from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('men', 'Men'),
    ('women', 'Women'),
    ('kids', 'Kids'),
    ('home', 'Home & Living'),
    ('shoes', 'Shoes'),
]

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    image = models.ImageField(upload_to='products/', default='path/to/default_image.jpg')
    # image_url = models.URLField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
