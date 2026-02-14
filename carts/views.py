from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from .models import Cart, CartItem

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    """Add a product to cart (supports color/size). If same variation exists, increment."""
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))

    # Accept from POST (product page) or GET (optional)
    color = (request.POST.get('color') or request.GET.get('color') or '').strip()
    size  = (request.POST.get('size')  or request.GET.get('size')  or '').strip()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, color=color, size=size)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(
            product=product, cart=cart, quantity=1, color=color, size=size
        )

    return redirect('cart')

def increase_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__cart_id=_cart_id(request))
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def decrease_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__cart_id=_cart_id(request))
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__cart_id=_cart_id(request))
    cart_item.delete()
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_items:
            total += (item.product.price * item.quantity)
            quantity += item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'store/cart.html', context)
