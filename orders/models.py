from django.db import models
from django.contrib.auth.models import User
from store.models import Product


PAYMENT_CHOICES = [
    ('cod', 'Cash on Delivery'),
    ('gateway', 'Payment Gateway'),
]


class Order(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders_app_orders'
    )
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    shipping_address = models.TextField()
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_CHOICES, blank=True, null=True
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='store_order_items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders_app_order_products'
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Deleted Product'}"


class ReturnRequest(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    )

    REFUND_STATUS_CHOICES = (
        ('Not Applicable', 'Not Applicable'),
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders_app_return_requests'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='return_requests'
    )
    item = models.ForeignKey(
        OrderItem,
        on_delete=models.CASCADE,
        related_name='return_requests',
        null=True,
        blank=True
    )
    reason = models.TextField()
    message = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Pending'
    )
    refund_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    refund_method = models.CharField(max_length=20, default='UPI', blank=True)
    upi_id = models.CharField(max_length=100, blank=True, null=True)
    refund_status = models.CharField(
        max_length=20, choices=REFUND_STATUS_CHOICES, default='Not Applicable'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return #{self.id} - Order #{self.order.id}"