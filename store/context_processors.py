from .models import Cart



def cart_count(request):
    """Inject cart item count into every template context."""
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'cart_count': count}
