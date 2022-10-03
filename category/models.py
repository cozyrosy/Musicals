from datetime import datetime
from distutils.command.upload import upload
from email.mime import image
from itertools import product
from operator import mod
from tkinter import CASCADE
from unicodedata import category
from django.db import models
import os
import datetime
from accounts.models import Account

# Create your models here.
def get_file_path(request, filename):
    original_filename = filename
    nowTime           = datetime.datetime.now().strftime('%Y%m%d%H:%M')
    filename          = "%s%s" % (nowTime,original_filename)
    return os.path.join('uploads/', filename)

class PriceFilter(models.Model):
    FILTER_PRICE = (
        ('1000 TO 10000', '1000 TO 10000'),
        ('10000 TO 20000', '10000 TO 20000'),
        ('20000 TO 30000', '20000 TO 30000'),
        ('30000 TO 40000', '30000 TO 40000'),
        ('40000 TO 50000', '40000 TO 50000'),
    )

    price = models.CharField(choices=FILTER_PRICE, max_length=60, default='default', null=True, blank=True)

    def __str__(self):
        return self.price

class Category(models.Model):
    category_name = models.CharField(max_length=50, default='default')
    slug          = models.SlugField(max_length=50,default='default')
    description   = models.TextField(max_length=255, blank=True,default='default')
    cat_image     = models.ImageField(upload_to ='photos/categories', blank=True)
    discount_amnt    = models.FloatField(null=True, blank=False)
   

    class Meta:
        verbose_name ='category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name 

    
class Product(models.Model):
    category          = models.ForeignKey(Category, on_delete=models.CASCADE)
    filter_pricee     = models.ForeignKey(PriceFilter, on_delete=models.CASCADE)
    slug              = models.CharField(max_length=150, null=True, blank=False)
    product_name      = models.CharField(max_length=150, null=True, blank=False)
    product_image     = models.ImageField(upload_to='photos/products', null=True, blank=False)
    product_image_1   = models.ImageField(upload_to='photos/products', null=True, blank=False)
    product_image_2   = models.ImageField(upload_to='photos/products', null=True, blank=False)
    description       = models.CharField(max_length=400, null=True, blank=False)
    quantity          = models.IntegerField(null=True, blank=False)
    orignal_price     = models.FloatField(null=True, blank=False)
    selling_price     = models.FloatField(null=True, blank=False)
    discount_price    = models.FloatField(null=True, blank=False)
    status            = models.BooleanField(default=False, help_text="0-default, 1=Hidden")
    trending          = models.BooleanField(default=False, help_text="0-default, 1=Trending")
    tag               = models.CharField(max_length=150, null=True, blank=False)
    is_featured       = models.BooleanField(default=False)
    filter_pricee     = models.ForeignKey(PriceFilter, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return self.product_name


class Coupon(models.Model):
    coupon_code    = models.CharField(max_length=20)
    is_expired     = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimun_amount = models.IntegerField(default=500)

class ProductOffer(models.Model):
    discount   = models.IntegerField(default=0)
    is_expired = models.BooleanField(default=True)
    product    = models.OneToOneField(Product,related_name='product_offer', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.product_name

class CategoryOffer(models.Model):
    discount_amnt   = models.IntegerField(default=0)
    is_expired      = models.BooleanField(default=True)
    category        = models.OneToOneField(Category,related_name='cat_offer',on_delete=models.CASCADE)

    def __str__(self):
        return self.category.category_name


