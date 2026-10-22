from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Product
from .models import CartItem


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def cart_view(request):
    # Logged-in user ke sare cart items fetch karein
    cart_items = CartItem.objects.filter(user=request.user)
    
    grand_total = 0

    # Total Price aur Grand Total Calculate karein
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        grand_total += item.total_price

    context = {
        'cart_items': cart_items,
        'grand_total': grand_total,
    }
    
    return render(request, 'cart/cart.html', context)


@login_required
def decrease_quantity(request, product_id):
    cart_item = get_object_or_404(
        CartItem,
        user=request.user,
        product_id=product_id
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


@login_required
def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(
        CartItem,
        user=request.user,
        product_id=product_id
    )

    cart_item.delete()

    return redirect('cart')


@login_required
def checkout(request):
    return render(request, 'checkout.html')