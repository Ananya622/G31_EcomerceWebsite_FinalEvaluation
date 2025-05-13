

# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Product
# from cart.models import Cart, CartItem
# from reviews.models import Review
# from django.contrib.auth.decorators import login_required

# def is_admin_or_brand(user):
#     return user.groups.filter(name__in=['Admin', 'Approved Brand']).exists()

# # Dynamic category view
# def category_view(request, category):
#     products = Product.objects.filter(category=category)
#     return render(request, f'products/{category}.html', {'products': products})

# # Product detail
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     return render(request, 'products/product_detail.html', {'product': product})

# # Add product (admin or brand)
# @login_required
# @user_passes_test(is_admin_or_brand)
# def add_product(request, category):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.category = category
#             product.created_by = request.user
#             product.save()
#             return redirect('admin_dashboard')
#     else:
#         form = ProductForm()
#     return render(request, 'products/add_product.html', {'form': form, 'category': category})

# # Edit product
# @login_required
# @user_passes_test(is_admin_or_brand)
# def edit_product(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.user != product.created_by:
#         return redirect('admin_dashboard')
    
#     form = ProductForm(request.POST or None, request.FILES or None, instance=product)
#     if form.is_valid():
#         form.save()
#         return redirect('admin_dashboard')

#     return render(request, 'products/edit_product.html', {'form': form})

# # Delete product
# @login_required
# @user_passes_test(is_admin_or_brand)
# def delete_product(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.user == product.created_by:
#         product.delete()
#     return redirect('admin_dashboard')





# def product_detail(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     reviews = Review.objects.filter(product=product)

#     if request.method == 'POST' and request.user.is_authenticated:
#         # Add to Cart logic
#         cart, created = Cart.objects.get_or_create(user=request.user)
#         cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

#         quantity = int(request.POST.get('quantity', 1))
#         cart_item.quantity += quantity
#         cart_item.save()

#         return redirect('cart:view_cart')

#     return render(request, 'products/product_detail.html', {
#         'product': product,
#         'reviews': reviews,
#     })





# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Product
# from cart.models import Cart, CartItem
# from reviews.models import Review
# from django.contrib.auth.decorators import login_required

# def is_admin_or_brand(user):
#     return user.groups.filter(name__in=['Admin', 'Approved Brand']).exists()

# # Dynamic category view
# def category_view(request, category):
#     products = Product.objects.filter(category=category)
#     return render(request, f'products/{category}.html', {'products': products})

# # Product detail (final version)
# def product_detail(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     reviews = Review.objects.filter(product=product)

#     if request.method == 'POST' and request.user.is_authenticated:
#         # Add to Cart logic
#         cart, created = Cart.objects.get_or_create(user=request.user)
#         cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

#         quantity = int(request.POST.get('quantity', 1))
#         cart_item.quantity += quantity
#         cart_item.save()

#         return redirect('cart:view_cart')

#     return render(request, 'products/product_detail.html', {
#         'product': product,
#         'reviews': reviews,
#     })








from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from cart.models import Cart, CartItem
from reviews.models import Review
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProductForm  # Import ProductForm to avoid errors in add_product view

# Check if user is admin or approved brand
def is_admin_or_brand(user):
    return user.groups.filter(name__in=['Admin', 'Approved Brand']).exists()

# Dynamic category view (filter products by category)
def category_view(request, category):
    products = Product.objects.filter(category=category)
    return render(request, f'products/{category}.html', {'products': products})

# Product detail (view product with reviews and add to cart functionality)
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product)

    if request.method == 'POST' and request.user.is_authenticated:
        # Add to Cart logic
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        quantity = int(request.POST.get('quantity', 1))
        cart_item.quantity += quantity
        cart_item.save()

        return redirect('cart:view_cart')

    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
    })

# Add product (admin or approved brand)
@login_required
@user_passes_test(is_admin_or_brand)
def add_product(request, category):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.category = category
            product.created_by = request.user
            product.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form, 'category': category})

# Edit product (admin or approved brand)
@login_required
@user_passes_test(is_admin_or_brand)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user != product.created_by:
        return redirect('admin_dashboard')
    
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('admin_dashboard')

    return render(request, 'products/edit_product.html', {'form': form})

# Delete product (admin or approved brand)
@login_required
@user_passes_test(is_admin_or_brand)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user == product.created_by:
        product.delete()
    return redirect('admin_dashboard')
