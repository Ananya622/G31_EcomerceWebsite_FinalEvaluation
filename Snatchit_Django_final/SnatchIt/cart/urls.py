# cart/urls.py
from django.urls import path
from . import views

app_name='cart'

urlpatterns = [
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('remove_item/<int:item_id>/', views.remove_item, name='remove_item'),
    path('update_cart_status/<int:cart_id>/', views.update_cart_status, name='update_cart_status'),  # Admin only
    path('admin/carts/', views.admin_cart_list, name='admin_cart_list'),
    path('admin/cart/<int:cart_id>/edit/', views.admin_edit_cart_status, name='admin_edit_cart_status'),
    path('order-success/', views.order_success, name='order_success'),
    path('order-history/', views.order_history, name='order_history'),

]
