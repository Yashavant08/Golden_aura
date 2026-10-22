from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from store.models import Product
from .models import Favorite

@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        favorite.delete()
    return redirect('product_detail', pk=product_id)

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user = request.user)

    return render(request, "favorites/favorites_list.html", {
        "favorites": favorites
    })