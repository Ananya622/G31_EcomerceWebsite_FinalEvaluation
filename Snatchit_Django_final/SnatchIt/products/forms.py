# products/forms.py

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price','stock', 'category','image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }