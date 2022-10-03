from django.contrib import admin
from . models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug':('category_name',)}
    list_display= ('category_name', 'slug')
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Coupon)
admin.site.register(ProductOffer)
admin.site.register(CategoryOffer)
admin.site.register(PriceFilter)