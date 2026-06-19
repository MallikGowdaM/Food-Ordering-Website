from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.db.models import Sum, Count
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import FoodItem, Cart, Order, OrderItem


# ─────────────────────────────────────────────
# Inline: Order Items inside Order detail
# ─────────────────────────────────────────────
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('food_name', 'food_price', 'quantity', 'get_subtotal')
    fields = ('food_name', 'food_price', 'quantity', 'get_subtotal')
    can_delete = False

    def get_subtotal(self, obj):
        return format_html('<strong>₹{}</strong>', obj.subtotal)
    get_subtotal.short_description = 'Subtotal'


# ─────────────────────────────────────────────
# FoodItem Admin
# ─────────────────────────────────────────────
@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'category', 'formatted_price', 'availability_badge', 'created_at')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('is_available',)
    ordering = ('category', 'name')
    readonly_fields = ('image_preview_large', 'created_at')
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'category', 'description', 'is_available')
        }),
        ('Pricing & Image', {
            'fields': ('price', 'image', 'image_preview_large')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:8px;" />', obj.image.url)
        return format_html('<span style="color:#ccc;">No Image</span>')
    image_preview.short_description = '📷 Photo'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:200px;max-height:200px;object-fit:cover;border-radius:12px;" />', obj.image.url)
        return "No image uploaded"
    image_preview_large.short_description = 'Current Image'

    def formatted_price(self, obj):
        return format_html('<strong style="color:#28a745;">₹{}</strong>', obj.price)
    formatted_price.short_description = '💰 Price'
    formatted_price.admin_order_field = 'price'

    def availability_badge(self, obj):
        if obj.is_available:
            return format_html('<span style="background:#28a745;color:white;padding:3px 10px;border-radius:20px;font-size:12px;">✅ Available</span>')
        return format_html('<span style="background:#dc3545;color:white;padding:3px 10px;border-radius:20px;font-size:12px;">❌ Unavailable</span>')
    availability_badge.short_description = 'Status'


# ─────────────────────────────────────────────
# Order Admin
# ─────────────────────────────────────────────
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_link', 'formatted_total', 'status_badge', 'payment_badge', 'phone', 'created_at')
    list_filter = ('status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'address', 'id')
    list_editable = ('status',)
    readonly_fields = ('user', 'total_price', 'payment_method', 'payment_status', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Order Info', {
            'fields': ('user', 'status', 'total_price')
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_status')
        }),
        ('Delivery', {
            'fields': ('address', 'phone', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def order_id(self, obj):
        return format_html('<strong>#{}  </strong>', obj.id)
    order_id.short_description = 'Order ID'
    order_id.admin_order_field = 'id'

    def customer_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    customer_link.short_description = '👤 Customer'

    def formatted_total(self, obj):
        return format_html('<strong>₹{}</strong>', obj.total_price)
    formatted_total.short_description = '💰 Total'
    formatted_total.admin_order_field = 'total_price'

    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'confirmed': '#17a2b8',
            'preparing': '#fd7e14',
            'out_for_delivery': '#6f42c1',
            'delivered': '#28a745',
            'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:20px;font-size:12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = '📦 Status'

    def payment_badge(self, obj):
        if obj.payment_status:
            return format_html('<span style="background:#28a745;color:white;padding:3px 10px;border-radius:20px;font-size:12px;">✅ Paid ({})</span>', obj.payment_method or 'N/A')
        return format_html('<span style="background:#dc3545;color:white;padding:3px 10px;border-radius:20px;font-size:12px;">⏳ Unpaid</span>')
    payment_badge.short_description = '💳 Payment'


# ─────────────────────────────────────────────
# Cart Admin
# ─────────────────────────────────────────────
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_item', 'quantity', 'cart_subtotal', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'food_item__name')
    readonly_fields = ('added_at',)

    def cart_subtotal(self, obj):
        return format_html('<strong>₹{}</strong>', obj.subtotal)
    cart_subtotal.short_description = 'Subtotal'


# ─────────────────────────────────────────────
# Enhance default User Admin
# ─────────────────────────────────────────────
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'full_name', 'is_staff', 'is_active', 'order_count', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or "—"
    full_name.short_description = 'Full Name'

    def order_count(self, obj):
        count = obj.orders.count()
        if count:
            url = reverse('admin:store_order_changelist') + f'?user__id__exact={obj.id}'
            return format_html('<a href="{}">{} order(s)</a>', url, count)
        return "0 orders"
    order_count.short_description = '📦 Orders'


# ─────────────────────────────────────────────
# Admin Site Customizations
# ─────────────────────────────────────────────
admin.site.site_title = "FoodieHub Admin"
admin.site.site_header = "🍔 FoodieHub Admin Panel"
admin.site.index_title = "Restaurant Management Dashboard"
