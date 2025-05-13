



from django.urls import path
from . import views

app_name='products'

urlpatterns = [
    path('category/<str:category>/', views.category_view, name='category_view'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/<str:category>/', views.add_product, name='add_product'),
    path('edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
]
