from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models
from .models import Product, Size, ProductImage, Wishlist, Order, OrderItem, ReturnRequest

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'size_type')
    list_filter = ('size_type',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'material', 'karat', 'weight', 'category', 'created_at')
    list_filter = ('material', 'karat', 'category', 'collection', 'gender')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]

    # Admin form me Size options ko clean Checkboxes ki tarah render karne ke liye
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price', 'image')
        }),
        ('Metal & Weight Details (Tanishq Style)', {
            'fields': ('material', 'karat', 'weight', 'metal_color', 'sizes')
        }),
        ('Stone / Diamond Details (Optional)', {
            'fields': ('diamond_carat',)
        }),
        ('Categorization, Gender & Occasion', {
            'fields': ('category', 'collection', 'gender', 'occasion')
        }),
    )
    
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    search_fields = ('user__username', 'product__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('full_name', 'email', 'tracking_number')

@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'user', 'status', 'refund_status', 'created_at')
    list_filter = ('status', 'refund_status')
    search_fields = ('order__id', 'user__username', 'upi_id')