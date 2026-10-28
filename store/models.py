from django.contrib.auth.models import User
from django.db import models

from django.contrib.auth.models import User
from django.db import models


# 1. Pehle Size model define hona chahiye
class Size(models.Model):
    SIZE_TYPE_CHOICES = [
        ('ring', 'Ring Size'),
        ('bangle', 'Bangle / Bracelet Size'),
        ('chain', 'Chain / Necklace Length'),
        ('general', 'General / Free Size'),
    ]
    
    name = models.CharField(max_length=50, help_text="e.g., Size 12, 2.4 Bangle, 18 Inch")
    size_type = models.CharField(max_length=20, choices=SIZE_TYPE_CHOICES, default='ring')

    class Meta:
        ordering = ['size_type', 'name']

    def __str__(self):
        return f"{self.get_size_type_display()} - {self.name}"


from django.db import models
from django.contrib.auth.models import User

# 1. Size model pehle define hai
class Size(models.Model):
    SIZE_TYPE_CHOICES = [
        ('ring', 'Ring Size'),
        ('bangle', 'Bangle / Bracelet Size'),
        ('chain', 'Chain / Necklace Length'),
        ('general', 'General / Free Size'),
    ]
    
    name = models.CharField(max_length=50, help_text="e.g., Size 12, 2.4 Bangle, 18 Inch")
    size_type = models.CharField(max_length=20, choices=SIZE_TYPE_CHOICES, default='ring')

    class Meta:
        ordering = ['size_type', 'name']

    def __str__(self):
        return f"{self.get_size_type_display()} - {self.name}"


# 2. Product model (Metal Color Dropdown ke saath)
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('rings', 'Rings'),
        ('pendants', 'Pendants'),
        ('chains', 'Chains'),
        ('earrings', 'Earrings'),
        ('necklaces', 'Necklaces'),
        ('bracelets', 'Bracelets'),
        ('bangles', 'Bangles'),
        ('solitaires', 'Solitaires'),
    ]

    COLLECTION_CHOICES = [
        ('bridal', 'Bridal Wear'),
        ('daily', 'Daily Wear'),
        ('party', 'Party Wear'),
        ('office', 'Office Wear'),
        ('kids', 'Kids Wear'),
        ('festival', 'Special Festival'),
    ]

    GENDER_CHOICES = [
        ('women', 'Women'),
        ('men', 'Men'),
    ]

    MATERIAL_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('diamond', 'Diamond'),
    ]

    KARAT_CHOICES = [
        ('18k', '18KT Gold'),
        ('22k', '22KT Gold'),
        ('24k', '24KT Pure Gold'),
        ('925', '925 Sterling Silver'),
        ('vvs', 'VVS Diamond'),
    ]

    # 🌟 NEW DROPDOWN CHOICES FOR METAL COLOR
    METAL_COLOR_CHOICES = [
        ('Yellow Gold', 'Yellow Gold'),
        ('White Gold', 'White Gold'),
        ('Rose Gold', 'Rose Gold'),
        ('Sterling Silver', 'Sterling Silver'),
        ('Oxidised Silver', 'Oxidised Silver'),
        ('Platinum Finish', 'Platinum Finish'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='rings')
    collection = models.CharField(max_length=100, choices=COLLECTION_CHOICES, default='daily', blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='women')

    material = models.CharField(max_length=50, choices=MATERIAL_CHOICES, default='gold')
    karat = models.CharField(max_length=50, choices=KARAT_CHOICES, default='22k')

    # Tanishq-Style Weight & Details Fields
    weight = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, help_text="Gross Weight in grams (e.g., 5.450)")
    
    # 🌟 Metal Color converted to clean Dropdown Menu
    metal_color = models.CharField(max_length=50, choices=METAL_COLOR_CHOICES, default='Yellow Gold', blank=True, null=True)
    
    diamond_carat = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 0.084 ct (Leave blank if no diamond)")
    occasion = models.CharField(max_length=100, default='Daily Wear', blank=True, null=True, help_text="e.g., Casual Wear, Bridal, Festive")

    # Sizes ManyToMany Field
    sizes = models.ManyToManyField(Size, blank=True, help_text="Select available sizes for this product")

    image = models.ImageField(upload_to='product/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Direct image link (e.g. Unsplash URL)")

    def __str__(self):
        return f"{self.product.name} Image"


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store_orders')
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    shipping_address = models.TextField()
    payment_method = models.CharField(max_length=20, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
  
    # 🔒 High-Value Secure Jewellery Delivery Fields
    courier_name = models.CharField(max_length=100, default='Sequel / BVC Secure Logistics', blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    delivery_otp = models.CharField(max_length=6, blank=True, null=True)
    is_insured = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order #{self.id} - {self.full_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='store_order_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='store_order_products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name if self.product else "Deleted Product"}'


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'


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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='return_requests')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='return_requests')
    item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='return_requests')
    reason = models.TextField()
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    refund_method = models.CharField(max_length=20, default='UPI', blank=True)
    upi_id = models.CharField(max_length=100, blank=True, null=True)
    refund_status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default='Not Applicable')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Return #{self.id} - Order #{self.order.id}'