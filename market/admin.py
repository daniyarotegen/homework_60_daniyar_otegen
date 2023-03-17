from django.contrib import admin
from market.models import Product, Order, OrderItem


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image', 'category', 'quantity', 'price')
    search_fields = ('name', 'category')
    list_filter = ('name', 'category',)
    ordering = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'address', 'phone', 'created_at')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
