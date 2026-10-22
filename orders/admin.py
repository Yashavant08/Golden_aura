from django.contrib import admin
from .models import Order, OrderItem, ReturnRequest


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'full_name',
        'total_amount',
        'payment_method',
        'status',
        'created_at'
    )

    list_editable = (
        'status',
    )

    list_filter = (
        'status',
        'payment_method',
        'created_at'
    )

    search_fields = (
        'id',
        'user__username',
        'full_name',
        'mobile_number'
    )

    inlines = [
        OrderItemInline
    ]


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'order',
        'status',
        'refund_status',
        'refund_amount',
        'created_at'
    )

    list_editable = ('status', 'refund_status')      # <-- ye nayi line

    list_filter = (
        'status',
        'refund_status',
        'created_at'
    )

    search_fields = (
        'user__username',
        'order__id',
        'reason'
    )