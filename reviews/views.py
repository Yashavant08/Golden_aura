from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from store.models import Product
from .models import Review


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        comment = request.POST.get('comment')

    if not rating and not title and not comment:
        return redirect('product_detail', pk=product.id)

    existing_review = Review.objects.filter(
        user=request.user,
        product=product
    ).first()

    if existing_review is None:
        Review.objects.create(
                user=request.user,
                product=product,
                rating=rating,
                title=title,
                comment=comment
            )
    else:
        existing_review.rating = rating
        existing_review.title = title
        existing_review.comment = comment
        existing_review.save()

        return redirect('product_detail', pk=product.id)

    return redirect('product_detail', pk=product.id)