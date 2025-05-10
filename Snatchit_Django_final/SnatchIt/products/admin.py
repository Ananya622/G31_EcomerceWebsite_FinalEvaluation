from django.contrib import admin

# Register your models here.

from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price','stock', 'category', 'created_by', 'image')
    fields = ('title', 'description', 'price', 'stock', 'category', 'image', 'created_by')