from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.auth_page, name='auth_page'),
    path('redirect/', views.role_redirect, name='role_redirect'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('farmer-dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('logout/', views.logout_view, name='logout'),

]
