# cart/admin.py
# from django.contrib import admin
# from .models import Cart, CartItem

# class CartItemInline(admin.TabularInline):
#     model = CartItem
#     extra = 0

# class CartAdmin(admin.ModelAdmin):
#     list_display = ('user', 'created_at', 'total_cost')
#     inlines = [CartItemInline]

# admin.site.register(Cart, CartAdmin)
# admin.site.register(CartItem)



from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at', 'total_cost')
    list_filter = ('status', 'created_at')
    inlines = [CartItemInline]
    search_fields = ('user__username',)

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
