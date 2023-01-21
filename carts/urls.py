from django.urls import path
from . import views



urlpatterns = [
    path('', views.cart, name='cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart')
]
