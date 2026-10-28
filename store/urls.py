from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('categories/', views.category_page, name='categories'),
    path('categories-all/', views.category_page, name='category_page'),
    path('category/', views.category_page, name='category_page'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('admin/returns/', views.returns_view, name='admin_returns'),\
    path('order/return/<int:order_id>/', views.request_return, name='request_return'),
    path('order/return/<int:order_id>/',views.request_return,name='request_return'),
    path('return/refund/<int:return_id>/',views.refund_details,name='refund_details'),
    path('return/manage/<int:return_id>/',views.manage_return_request,name='manage_return_request'),
    path('returns/',views.returns_view,name='return_requests'),
    path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    
    # Order Status Update Path (Admin Dashboard)
    path('admin-dashboard/update-status/<int:pk>/', views.update_order_status, name='update_order_status'),

    # Password Reset Paths
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/pass_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/pass_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/pass_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/pass_reset_complete.html'), name='password_reset_complete'),

    # Wishlist Paths
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('order/invoice/<int:order_id>/', views.order_invoice, name='order_invoice'),
    path('wishlist/', views.wishlist_page, name='wishlist_page'),
]