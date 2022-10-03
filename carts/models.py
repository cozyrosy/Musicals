
from hashlib import blake2s
from django.db import models

from category.models import *

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class cartItem(models.Model):
    user      = models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    cart      = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    coupon    = models.ForeignKey(Coupon,on_delete=models.SET_NULL, null=True, blank=True)
    quantity  = models.IntegerField( null=True)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        if self.product.discount_price:
            return (self.product.orignal_price - self.product.discount_price ) * self.quantity 
        else:
            return self.product.orignal_price * self.quantity

    def __str__(self):
        return str(self.product) 