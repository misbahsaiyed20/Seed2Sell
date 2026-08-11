from django.urls import path
from . import views
from .views import download_invoice

urlpatterns = [

    path('', views.index, name='index'),
    path('dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('shop/', views.shop, name='shop'),
    path('shop/category/<int:category_id>/', views.shop_by_category, name='shop_by_category'),
    path('shop/<int:pk>/', views.shop_detail, name='shop_detail'),
    path('farmer/orders/', views.farmer_orders, name='farmer_orders'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/increase/<int:product_id>/', views.increase_cart, name='increase_cart'),
    path('cart/decrease/<int:product_id>/', views.decrease_cart, name='decrease_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('my-orders/', views.order_history, name='order_history'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('farmer/add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('invoice/<int:order_id>/', download_invoice, name='download_invoice'),
    path('upi-payment/<int:order_id>/', views.upi_payment, name='upi_payment'),
    path(
        'upi/<int:order_id>/<str:app>/',
        views.upi_app_payment,
        name='upi_app'
    ),
    path(
        'upi-processing/<int:order_id>/',
        views.upi_processing,
        name='upi_processing'
    ),



]


