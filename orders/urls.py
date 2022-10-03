from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order' ),
    # path('razorPay/', views.razorPay, name='razorPay'),
    path('orders/', views.orders, name='orders'),
    path('orderView/<str:id>',views.orderView, name='orderView'),
    path('orderComplete/',views.orderComplete, name='orderComplete/'),
    path('orderInvoice/', views.order_invoice, name='order_invoice'),
    path('orderCancel/<str:id>',views.orderCancel, name='orderCancel'),
    path('orderReturn/<str:id>',views.orderReturn, name='orderReturn'),
    path('payPal/', views.payPal, name='payPal'),
    path('paymentMethod/',views.paymentMethod, name="paymentMethod")
]