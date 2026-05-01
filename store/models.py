from django.db import models
from django.contrib.auth.models import User


class FoodItem(models.Model):
    """Represents a food item available in the menu."""
    CATEGORY_CHOICES = [
        ('starters', 'Starters'),
        ('main_course', 'Main Course'),
        ('desserts', 'Desserts'),
        ('beverages', 'Beverages'),
        ('snacks', 'Snacks'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='main_course')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'name']


class Cart(models.Model):
    """Represents a cart item for a specific user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.food_item.name} x{self.quantity}"

    @property
    def subtotal(self):
        return self.food_item.price * self.quantity

    class Meta:
        unique_together = ('user', 'food_item')


class Order(models.Model):
    """Represents a placed order."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    address = models.TextField()
    phone = models.CharField(max_length=15)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} - {self.status}"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    """Represents individual items within an order (snapshot at time of order)."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True)
    food_name = models.CharField(max_length=200)   # Snapshot of name
    food_price = models.DecimalField(max_digits=8, decimal_places=2)  # Snapshot of price
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.food_name} x{self.quantity}"

    @property
    def subtotal(self):
        return self.food_price * self.quantity
