from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Review
from products.models import Product
from django.contrib.auth.decorators import login_required

@login_required
def submit_review(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        rating = request.POST['rating']
        review_text = request.POST['review_text']

        review = Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            review_text=review_text
        )

        return redirect('products:product_detail', product_id=product.id)
