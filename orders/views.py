from decimal import Decimal

import razorpay
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from cart.models import CartItem
from .models import Order, OrderItem, ReturnRequest
from store.models import Product   # Product agar store app me hai


def get_razorpay_client():
    return razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )


def calculate_totals(cart_items):
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    gst = subtotal * Decimal('0.03')
    return subtotal, gst, subtotal + gst


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    subtotal, gst, grand_total = calculate_totals(cart_items)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        mobile_number = request.POST.get('phone')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        state = request.POST.get('state')
        payment_method = request.POST.get('payment_method')

        complete_address = f"{address}, {city}, {state} - {pincode}"

        # ---------- CASH ON DELIVERY ----------
        if payment_method == 'cod':
            order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                email=request.user.email,
                mobile_number=mobile_number,
                shipping_address=complete_address,
                payment_method='cod',
                total_amount=grand_total,
                status='Pending',
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
            cart_items.delete()
            messages.success(request, f"Order #{order.id} placed successfully!")
            return redirect('order_success')

        # ---------- ONLINE PAYMENT ----------
        elif payment_method == 'online':
            request.session['shipping_details'] = {
                'full_name': full_name,
                'mobile_number': mobile_number,
                'address': complete_address,
            }

    # GET request ya online payment: Razorpay order banao aur page dikhao
    amount_in_paise = int(grand_total * 100)
    razorpay_order = get_razorpay_client().order.create({
        "amount": amount_in_paise,
        "currency": "INR",
        "payment_capture": 1,
    })

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'gst': gst,
        'grand_total': grand_total,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'razorpay_amount': amount_in_paise,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def payment_success(request):
    payment_id = (
        request.GET.get('payment_id')
        or request.GET.get('razorpay_payment_id')
    )

    cart_items = CartItem.objects.filter(user=request.user)

    # Cart already khali hai to bas success page dikha do
    if not cart_items.exists():
        return render(request, 'orders/order_success.html',
                      {'payment_id': payment_id})

    shipping = request.session.get('shipping_details', {})
    subtotal, gst, grand_total = calculate_totals(cart_items)

    order = Order.objects.create(
        user=request.user,
        full_name=shipping.get(
            'full_name',
            request.user.get_full_name() or request.user.username
        ),
        email=request.user.email,
        mobile_number=shipping.get('mobile_number'),
        shipping_address=shipping.get('address', 'Online Payment Address'),
        payment_method='gateway',
        total_amount=grand_total,
        status='Pending',
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

    cart_items.delete()
    request.session.pop('shipping_details', None)

    messages.success(
        request, f"Order #{order.id} placed successfully via Online Payment!"
    )
    return render(request, 'orders/order_success.html',
                  {'payment_id': payment_id, 'order': order})


def order_success(request):
    payment_id = request.GET.get('payment_id')
    return render(request, 'orders/order_success.html',
                  {'payment_id': payment_id})


@login_required
def admin_dashboard(request):
    return_requests = ReturnRequest.objects.all().order_by('-id')

    if request.method == 'POST' and 'action_return_id' in request.POST:
        ret_req = get_object_or_404(
            ReturnRequest, id=request.POST.get('action_return_id')
        )
        new_status = request.POST.get('new_status')  # Approved / Rejected
        ret_req.status = new_status
        ret_req.save()
        messages.success(
            request,
            f"Return request #{ret_req.id} status updated to {new_status}"
        )
        return redirect('admin_dashboard')

    orders = Order.objects.all().order_by('-id')
    products = Product.objects.all()

    total_revenue = orders.aggregate(s=Sum('total_amount'))['s'] or 0
    total_orders = orders.count()
    total_customers = User.objects.filter(is_staff=False).count()
    total_products = products.count()

    # Aaj ki sales (Order me created_at field maan ke chala hu)
    today = timezone.localdate()
    todays_sales = orders.filter(
        created_at__date=today
    ).aggregate(s=Sum('total_amount'))['s'] or 0

    context = {
        'orders': orders,
        'recent_orders': orders,
        'products': products,
        'return_requests': return_requests,
        'total_revenue': total_revenue,
        'todays_sales': todays_sales,
        'today_sales': todays_sales,
        'today_revenue': todays_sales,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'customers_count': total_customers,
        'total_users': total_customers,
        'total_products': total_products,
        'jewellery_count': total_products,
    }
    return render(request, 'orders/admin_dashboard.html', context)


@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid = [c[0] for c in getattr(Order, 'STATUS_CHOICES', [])]

        if not valid or new_status in valid:
            order.status = new_status
            order.save()
            messages.success(
                request, f'Order #{order.id} status updated to {new_status}!'
            )
        else:
            messages.error(request, 'Invalid status selected.')

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'store/my_orders.html', {'orders': orders})


@login_required
def request_return(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status.lower() != 'delivered':
        messages.error(
            request, "Only delivered orders are eligible for return/exchange."
        )
        return redirect('my_orders')

    items = order.store_order_items.all()

    if request.method == 'POST':
        reason = request.POST.get('reason')
        comments = request.POST.get('comments')
        item_id = request.POST.get('item_id')

        # Template ne item_id bheja to wo item, warna order ka pehla item
        if item_id:
            item = get_object_or_404(items, id=item_id)
        else:
            item = items.first()

        if reason and item:
            ReturnRequest.objects.create(
                user=request.user,
                order=order,
                item=item,
                reason=reason,
                message=comments,
                refund_amount=item.price * item.quantity,
                status='Pending',
            )
            messages.success(
                request,
                "Return request submitted successfully. Our team will contact you soon."
            )
            return redirect('my_orders')

        messages.error(request, "Please select a reason.")

    return render(
        request,
        'store/return_request.html',
        {'order': order, 'items': items}
    )
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