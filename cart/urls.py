from django.urls import path
from . import views

urlpatterns = [
    path('<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('', views.cart_view, name='cart'),
    path('decrease/<int:product_id>/', views.decrease_quantity,name='decrease_quantity'),
    path('remove/<int:product_id>/', views.remove_from_cart,name='remove_from_cart'),
    path('checkout/' , views.checkout, name='checkout'),
]