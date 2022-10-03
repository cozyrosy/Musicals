from email import message
from itertools import product
from re import T
from sre_parse import State
from tkinter import CASCADE
from django.db import models
from accounts.models import *
from category.models import *

# Create your models here.

class Payment(models.Model):
    user           = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id     = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid    = models.CharField(max_length=100)#this is the total amount paid
    status         = models.CharField(max_length=100)
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
 
class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    fname = models.CharField(max_length=150, null=True)
    lname = models.CharField(max_length=150, null=True)
    email = models.CharField(max_length=150, null=True)
    phone = models.CharField(max_length=150, null=True)
    address = models.TextField(null=True)
    country = models.CharField(max_length=150, null=True)
    state = models.CharField(max_length=150, null=True)
    city = models.CharField(max_length=150, null=True)
    pincode = models.CharField(max_length=150, null=True)
    total_price = models.FloatField(null=True)
    payment_mode = models.CharField(max_length=150, null=True)
    payment_id= models.CharField(max_length=250, null=True)
    orderstatuses = (
        ('Order Confirmed','Order Confirmed'),
        ('Order Shipped','Order Shipped'),
        ('Out for delivery','Out for delivery'),
        ('Order Delivered','Order Delivered')
    )
    status = models.CharField(max_length=150, choices=orderstatuses, default='Order Confirmed')
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) :
        return '{} - {}'.format(self.id, self.tracking_no)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name




