
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test
import requests

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, status='Pending')
    quantity = int(request.POST.get('quantity', 1))

    if quantity > product.stock:
        messages.error(request, f"Only {product.stock} item(s) available in stock.")
        return redirect('product_detail', product_id=product.id)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if cart_item.quantity + quantity > product.stock:
        messages.error(request, f"Adding {quantity} would exceed available stock. You already have {cart_item.quantity} in cart.")
        return redirect('product_detail', product_id=product.id)

    cart_item.quantity += quantity
    cart_item.save()
    update_cart_session_count(request)
    return redirect('cart:view_cart')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user, status='Pending')
    return render(request, 'cart/view_cart.html', {'cart': cart})


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user, status='Pending')

    if request.method == 'POST':
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        for item in cart.items.all():
            if item.quantity > item.product.stock:
                messages.error(request, f"Not enough stock for {item.product.title}. Available: {item.product.stock}")
                return redirect('cart:view_cart')

        ordered_items = []
        total_cost = 0
        for item in cart.items.all():
            item_total = float(item.quantity * item.product.price)
            ordered_items.append({
                'title': item.product.title,
                'image': item.product.image.url,
                'quantity': item.quantity,
                'price': float(item.product.price),
                'total_price': item_total
            })
            total_cost += item_total
            item.decrease_stock()

        # Update cart status
        cart.status = 'Shipped'
        cart.save()

        # Create Order
        order = Order.objects.create(
            user=request.user,
            address=address,
            payment_method=payment_method,
            total=total_cost,
            status='Pending'
        )

        # Create OrderItems
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear cart
        cart.items.all().delete()
        update_cart_session_count(request)

        # Store summary for success page
        request.session['order_summary'] = {
            'items': ordered_items,
            'address': address,
            'payment_method': payment_method,
            'total': total_cost
        }

        return redirect('cart:order_success')

    return render(request, 'cart/checkout.html', {'cart': cart})


@login_required
def order_success(request):
    order_summary = request.session.get('order_summary')
    if not order_summary:
        return redirect('index')
    return render(request, 'cart/order_success.html', {'order': order_summary})


@require_POST
@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = max(int(request.POST.get('quantity', 1)), 1)

    if quantity > item.product.stock:
        messages.error(request, f"Cannot update. Only {item.product.stock} item(s) available in stock.")
        return redirect('cart:view_cart')

    item.quantity = quantity
    item.save()
    update_cart_session_count(request)
    return redirect('cart:view_cart')


@require_POST
@login_required
def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    update_cart_session_count(request)
    return redirect('cart:view_cart')




def is_admin_or_approved(user):
    return user.groups.filter(name__in=['Admin', 'Approved Brand']).exists()



def update_cart_session_count(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, status='Pending')
        request.session['cart_items'] = cart.items.count()





def user_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()




@login_required
def order_history(request):
    user = request.user
    # For admins and approved brands, show all orders
    if user.is_superuser or user_in_group(user, "Admin") or user_in_group(user, "Approved Brand"):
        orders = Order.objects.all().order_by('-created_at')
    else:
        # For regular users, show only their orders
        orders = Order.objects.filter(user=user).order_by('-created_at')
    
    # Get status choices for the dropdown
    status_choices = Order.STATUS_CHOICES
    
    return render(request, 'cart/order_history.html', {
        'orders': orders,
        'status_choices': status_choices
    })

@login_required
@user_passes_test(lambda u: u.is_superuser or user_in_group(u, "Admin") or user_in_group(u, "Approved Brand"))
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status selected.")
            
    return redirect('cart:order_history')