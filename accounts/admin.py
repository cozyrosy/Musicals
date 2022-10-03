from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import Account, UserAddressBook


# Register your models here.

class AccountAdmin(UserAdmin):
    list_display= ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')

    filter_horizontal = ()
    list_filter = ()
    fieldsets= ()
admin.site.register(Account, AccountAdmin)

class UserAddressBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'lname', 'phone','address', 'country','state','city', 'pincode')
admin.site.register(UserAddressBook,UserAddressBookAdmin)