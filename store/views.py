from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from datetime import timedelta
from django.utils import timezone

from .models import Product, Wishlist
from orders.models import Order, OrderItem, ReturnRequest
from favorites.models import Favorite
from reviews.models import Review


# =========================
# HOME PAGE
# =========================
def home_view(request):
    category_slug = request.GET.get('category')
    gender_param = request.GET.get('gender')

    products = Product.objects.all()

    if gender_param in ['men', 'women']:
        current_gender = gender_param
    elif (
        request.user.is_authenticated
        and hasattr(request.user, 'profile')
        and request.user.profile.gender
    ):
        current_gender = request.user.profile.gender
    else:
        current_gender = 'women'

    if current_gender:
        products = products.filter(
            gender__iexact=current_gender
        )

    if category_slug:
        products = products.filter(
            category__iexact=category_slug
        )

    context = {
        'products': products,
        'current_gender': current_gender,
        'selected_category': category_slug,
    }

    return render(
        request,
        'store/home.html',
        context
    )


# =========================
# PRODUCT LIST
# =========================
def product_list(request):
    gender = request.GET.get('gender')
    category = request.GET.get('category')

    products = Product.objects.all()

    if gender:
        products = products.filter(
            gender__iexact=gender
        )

    if category:
        products = products.filter(
            category__iexact=category
        )

    context = {
        'products': products,
    }

    return render(
        request,
        'store/product_list.html',
        context
    )


# =========================
# PRODUCT DETAIL
# =========================
def product_detail(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk
    )

    is_favorite = False

    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            product=product
        ).exists()

    reviews = Review.objects.filter(
        product=product
    )

    context = {
        'product': product,
        'is_favorite': is_favorite,
        'reviews': reviews,
    }

    return render(
        request,
        'store/product_detail.html',
        context
    )


# =========================
# CATEGORIES PAGE
# =========================
def category_page(request):
    collection_name = request.GET.get('collection')
    gender_name = request.GET.get('gender')

    products = Product.objects.all()

    if collection_name and collection_name != 'ALL':
        products = products.filter(
            collection__iexact=collection_name
        )

    if gender_name:
        gender_name = gender_name.strip()

        products = products.filter(
            gender__iexact=gender_name
        )

    user_wishlist_ids = []

    if request.user.is_authenticated:
        user_wishlist_ids = list(
            Wishlist.objects.filter(
                user=request.user
            ).values_list(
                'product_id',
                flat=True
            )
        )

    context = {
        'products': products,
        'active_collection': collection_name,
        'active_gender': gender_name,
        'user_wishlist_ids': user_wishlist_ids,
    }

    return render(
        request,
        'store/categories.html',
        context
    )


# =========================
# TOGGLE WISHLIST
# =========================
@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id
    )

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        wishlist_item.delete()
        added = False
    else:
        added = True

    return JsonResponse({
        'added': added
    })


# =========================
# WISHLIST PAGE
# =========================
@login_required
def wishlist_page(request):
    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related(
        'product'
    )

    context = {
        'wishlist_items': wishlist_items
    }

    return render(
        request,
        'store/wishlist.html',
        context
    )


# =========================
# DASHBOARD
# =========================
@login_required
def dashboard_view(request):
    user_orders = Order.objects.filter(
        user=request.user
    ).order_by('-id')

    context = {
        'customer_orders': user_orders,
    }

    return render(
        request,
        'store/dashboard.html',
        context
    )


# =========================
# CUSTOMER DASHBOARD
# =========================
@login_required
def dashboard(request):
    user_orders = Order.objects.filter(
        user=request.user
    ).order_by('-id')

    today = timezone.now()

    for order in user_orders:

        order_date = None

        for date_field in [
            'created_at',
            'ordered_date',
            'date',
            'timestamp',
            'created'
        ]:

            if (
                hasattr(order, date_field)
                and getattr(order, date_field)
            ):
                order_date = getattr(
                    order,
                    date_field
                )
                break

        if order_date:

            return_deadline = (
                order_date + timedelta(days=15)
            )

            order.is_returnable = (
                getattr(order, 'status', '') == 'Delivered'
                and today <= return_deadline
            )

        else:
            order.is_returnable = False

    context = {
        'customer_orders': user_orders,
        'orders': user_orders,
    }

    return render(
        request,
        'store/dashboard.html',
        context
    )


# =========================
# PROFILE
# =========================
def profile_view(request):
    if request.user.is_authenticated:
        return render(
            request,
            'store/dashboard.html'
        )

    return redirect('login')


# =========================
# LOGOUT
# =========================
def custom_logout_view(request):
    logout(request)

    messages.info(
        request,
        'You have been successfully logged out.'
    )

    return redirect('login')


# =========================
# UPDATE ORDER STATUS
# ADMIN
# =========================
@login_required
def update_order_status(request, pk):

    if not request.user.is_staff:
        messages.error(
            request,
            "Access Denied: You do not have permission to perform this action."
        )

        return redirect('home')

    order = get_object_or_404(
        Order,
        pk=pk
    )

    if request.method == 'POST':

        new_status = request.POST.get('status')

        valid_statuses = [
            choice[0]
            for choice in Order.STATUS_CHOICES
        ]

        if new_status in valid_statuses:

            order.status = new_status
            order.save()

            messages.success(
                request,
                f"Order #{order.id} status updated successfully."
            )

        else:

            messages.error(
                request,
                "Invalid status selected."
            )

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            'dashboard'
        )
    )


# =========================
# RETURN REQUESTS
# ADMIN
# =========================
@staff_member_required
def returns_view(request):

    return_requests = ReturnRequest.objects.select_related(
        'user',
        'order',
        'item',
        'item__product'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'store/return_requests.html',
        {
            'return_requests': return_requests
        }
    )

from django.utils import timezone
from datetime import timedelta

# =========================
# REQUEST RETURN
# =========================
@login_required
def request_return(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    # 1. Check karo ki order delivered hai ya nahi
    if order.status.lower() != 'delivered':
        messages.error(
            request,
            'Sirf delivered products ke liye hi return request submit ki ja sakti hai.'
        )
        return redirect('dashboard')

    # 2. Strict 24-Hour (1 Day) Return Window Check
    # Agar model me delivered_at field hai toh wo use hogi, warna updated_at
    delivery_time = getattr(order, 'delivered_at', None) or order.updated_at
    if delivery_time:
        if timezone.now() - delivery_time > timedelta(hours=24):
            messages.error(
                request,
                'Return window expired! Delivery ke 24 ghante ke andar hi return request ki ja sakti hai.'
            )
            return redirect('dashboard')

    order_items = OrderItem.objects.filter(
        order=order
    )

    if request.method == 'POST':

        # Extra safety check for POST request submission
        if delivery_time and (timezone.now() - delivery_time > timedelta(hours=24)):
            messages.error(
                request,
                'Return window expired! Request process nahi ki ja sakti.'
            )
            return redirect('dashboard')

        item_id = request.POST.get('item_id')
        reason = request.POST.get('reason')
        message = request.POST.get(
            'message',
            ''
        ).strip()

        item = get_object_or_404(
            OrderItem,
            id=item_id,
            order=order
        )

        # Refund amount for selected product
        refund_amount = (
            item.price * item.quantity
        )

        ReturnRequest.objects.create(
            user=request.user,
            order=order,
            item=item,
            reason=reason,
            message=message,
            status='Pending',
            refund_amount=refund_amount,
            refund_method='UPI',
            refund_status='Pending'
        )

        messages.success(
            request,
            'Your return request has been submitted successfully.'
        )

        return redirect(
            'dashboard'
        )

    context = {
        'order': order,
        'order_items': order_items,
    }

    return render(
        request,
        'store/return_submit.html',
        context
    )

# =========================
# REFUND DETAILS
# =========================
@login_required
def refund_details(request, return_id):

    return_request = get_object_or_404(
        ReturnRequest,
        id=return_id,
        user=request.user
    )

    # Only approved requests can continue
    if return_request.status != 'Approved':

        messages.warning(
            request,
            'Your return request is not approved yet.'
        )

        return redirect(
            'dashboard'
        )

    if request.method == 'POST':

        upi_id = request.POST.get(
            'upi_id',
            ''
        ).strip()

        if not upi_id:

            messages.error(
                request,
                'Please enter your UPI ID.'
            )

            return redirect(
                'refund_details',
                return_id=return_request.id
            )

        return_request.upi_id = upi_id
        return_request.refund_method = 'UPI'
        return_request.refund_status = 'Processing'

        return_request.save()

        messages.success(
            request,
            'Refund details submitted successfully.'
        )

        return redirect(
            'dashboard'
        )

    return render(
        request,
        'store/refund_details.html',
        {
            'return_request': return_request
        }
    )


# =========================
# MANAGE RETURN REQUEST
# ADMIN
# =========================
@staff_member_required
def manage_return_request(request, return_id):

    return_request = get_object_or_404(
        ReturnRequest,
        id=return_id
    )

    if request.method == 'POST':

        action = request.POST.get(
            'action'
        )

        # APPROVE
        if action == 'approve':

            return_request.status = 'Approved'
            return_request.refund_status = 'Pending'

            return_request.save()

            messages.success(
                request,
                f'Return request #{return_request.id} approved.'
            )

        # REJECT
        elif action == 'reject':

            return_request.status = 'Rejected'
            return_request.refund_status = 'Not Applicable'

            return_request.save()

            messages.warning(
                request,
                f'Return request #{return_request.id} rejected.'
            )

        # COMPLETE
        elif action == 'complete':

            return_request.status = 'Completed'
            return_request.refund_status = 'Completed'

            return_request.save()

            messages.success(
                request,
                f'Refund for request #{return_request.id} marked completed.'
            )

        return redirect(
            'return_requests'
        )

    return render(
        request,
        'store/manage_return_request.html',
        {
            'return_request': return_request
        }
    )


# =========================
# ORDER INVOICE
# =========================
@login_required
def order_invoice(request, order_id):
    if request.user.is_staff:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = get_object_or_404(Order, id=order_id, user=request.user)

    # Items fetch logic
    items = getattr(order, 'store_order_items', None)
    if items:
        items = items.all()
    else:
        items = getattr(order, 'items', None)
        items = items.all() if items else []

    # Total amount calculation
    calculated_total = getattr(order, 'total', None) or getattr(order, 'total_amount', None) or getattr(order, 'amount', 0)

    context = {
        'order': order,
        'items': items,
        'calculated_total': calculated_total,
    }

    # Dono ke liye Single Uniform Template Path:
    return render(request, 'store/invoice.html', context)