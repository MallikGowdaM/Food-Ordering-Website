from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import transaction
from decimal import Decimal

from .models import FoodItem, Cart, Order, OrderItem
from .forms import RegisterForm, PlaceOrderForm


# ─────────────────────────────────────────
# Home & Menu Views
# ─────────────────────────────────────────

def home(request):
    """Landing page with featured food items."""
    featured_items = FoodItem.objects.filter(is_available=True)[:8]
    return render(request, 'store/home.html', {'featured_items': featured_items})


def menu(request):
    """Full food menu page with category filter."""
    category_filter = request.GET.get('category', '')
    items = FoodItem.objects.filter(is_available=True)
    if category_filter:
        items = items.filter(category=category_filter)

    categories = FoodItem.CATEGORY_CHOICES
    return render(request, 'store/menu.html', {
        'food_items': items,
        'categories': categories,
        'selected_category': category_filter,
    })


# ─────────────────────────────────────────
# Authentication Views
# ─────────────────────────────────────────

def register_view(request):
    """User registration page."""
    if request.user.is_authenticated:
        return redirect('menu')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            return redirect('menu')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    """User login page."""
    if request.user.is_authenticated:
        return redirect('menu')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'menu')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'store/login.html', {'form': form})


def logout_view(request):
    """Logout and redirect to home."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# ─────────────────────────────────────────
# Cart Views
# ─────────────────────────────────────────

@login_required
def cart_view(request):
    """View the current user's cart."""
    cart_items = Cart.objects.filter(user=request.user).select_related('food_item')
    total = sum(item.subtotal for item in cart_items)
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


@login_required
def add_to_cart(request, food_id):
    """Add a food item to the cart or increment quantity."""
    food_item = get_object_or_404(FoodItem, id=food_id, is_available=True)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        food_item=food_item,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Added another {food_item.name} to your cart.')
    else:
        messages.success(request, f'{food_item.name} added to your cart!')

    # Redirect back to the referring page (menu or home)
    next_url = request.META.get('HTTP_REFERER', 'menu')
    return redirect(next_url)


@login_required
def update_cart(request, cart_id):
    """Update quantity or remove an item from the cart."""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    action = request.POST.get('action')

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            messages.info(request, f'{cart_item.food_item.name} removed from cart.')
    elif action == 'remove':
        cart_item.delete()
        messages.info(request, f'{cart_item.food_item.name} removed from cart.')

    return redirect('cart')


@login_required
def clear_cart(request):
    """Remove all items from the cart."""
    Cart.objects.filter(user=request.user).delete()
    messages.info(request, 'Your cart has been cleared.')
    return redirect('cart')


# ─────────────────────────────────────────
# Order Views
# ─────────────────────────────────────────

@login_required
def checkout_view(request):
    """Checkout page to place an order."""
    cart_items = Cart.objects.filter(user=request.user).select_related('food_item')

    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty. Add some food items first!')
        return redirect('menu')

    total = sum(item.subtotal for item in cart_items)

    if request.method == 'POST':
        form = PlaceOrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create the order
                order = Order.objects.create(
                    user=request.user,
                    total_price=total,
                    address=form.cleaned_data['address'],
                    phone=form.cleaned_data['phone'],
                    notes=form.cleaned_data.get('notes', ''),
                )
                # Create order items (snapshot of cart)
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        food_item=cart_item.food_item,
                        food_name=cart_item.food_item.name,
                        food_price=cart_item.food_item.price,
                        quantity=cart_item.quantity,
                    )
                # Clear the cart
                cart_items.delete()

            messages.success(request, f'🎉 Order #{order.id} placed successfully! We\'ll deliver soon.')
            return redirect('order_detail', order_id=order.id)
        else:
            messages.error(request, 'Please fill in all required fields.')
    else:
        form = PlaceOrderForm()

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'form': form,
    })


@login_required
def order_history(request):
    """View all past orders for the current user."""
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'store/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """View details of a specific order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})
