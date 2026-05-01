from django.contrib import admin
from .models import FoodItem, Cart, Order, OrderItem


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'created_at')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_available')
    ordering = ('category', 'name')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('food_name', 'food_price', 'quantity', 'subtotal')
    fields = ('food_name', 'food_price', 'quantity', 'subtotal')

    def subtotal(self, obj):
        return f"₹{obj.subtotal}"
    subtotal.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'phone', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'address')
    list_editable = ('status',)
    readonly_fields = ('user', 'total_price', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_item', 'quantity', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'food_item__name')
