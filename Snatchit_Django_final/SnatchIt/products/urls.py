# from django.urls import path
# from . import views

# urlpatterns = [
#      path('men/', views.men_products, name='men'),
#     path('women/', views.women_products, name='women'),
#     path('kids/', views.kids_products, name='kids'),
#     path('shoes/', views.shoes_products, name='shoes'),

#      path('<str:category>/', views.category_view, name='category_view'),
#     path('<int:pk>/', views.product_detail, name='product_detail'),
#     path('add/<str:category>/', views.add_product, name='add_product'),
#     path('edit/<int:pk>/', views.edit_product, name='edit_product'),
#     path('delete/<int:pk>/', views.delete_product, name='delete_product'),
# ]




# from django.urls import path
# from . import views

# urlpatterns = [
#     path('<str:category>/', views.category_view, name='category_view'),
#     path('add/<str:category>/', views.add_product, name='add_product'),
#     path('edit/<int:pk>/', views.edit_product, name='edit_product'),
#     path('delete/<int:pk>/', views.delete_product, name='delete_product'),
#     path('<int:product_id>/', views.product_detail, name='product_detail'),
# ]



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
