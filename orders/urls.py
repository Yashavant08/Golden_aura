from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),

    path('success/', views.order_success, name='order_success'),

    path(
        'payment-success/',
        views.payment_success,
        name='payment_success'
    ),

    path(
        'admin-dashboard/update-status/<int:order_id>/',
        views.update_order_status,
        name='update_order_status'
    ),

    path(
        'my-orders/',
        views.my_orders,
        name='my_orders'
    ),

    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),


    path(
        'order/return/<int:order_id>/',
        views.request_return,
        name='request_return'
    ),

    path( 'invoice/<int:order_id>/', views.order_invoice,name='order_invoice'),
]