from django.urls import path
from . import views

urlpatterns = [
    path('sad/', views.cartview, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),

    path('update-cart', views.updatecart, name="updatecart"),
    path('checkout/', views.checkout, name='checkout'),
]