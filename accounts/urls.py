from django.urls import path 
from . import views
from django.contrib.auth.views import LogoutView, PasswordChangeView


urlpatterns = [
    path('', views.loginView.as_view(), name="login"),
    path('homeee/', views.home, name="home"),
    path('register/', views.registerView.as_view(), name="register"),
    path('otpentersignup/<int:phone_number>/', views.otpentersignup, name="otpentersignup"),
    path('otpenterlogin/<int:phone_number>/', views.otpenterlogin, name="otpenterlogin"),
    path('otpLogin/', views.otpLogin, name="otpLogin"),

    path('<str:slug>/', views.collectionView, name="collectionView"),
    path('<str:cat_slug>/<str:prod_slug>', views.productView, name="productView"),

    path('userProfile', views.userProfile, name="userProfile"),
    path('editProfile', views.editProfile, name="editProfile"),
    path('my_addressbook', views.my_addressbook, name="my_addressbook"),
    path('save_address', views.save_address, name="save_address"),
    path('editAddress/<int:id>/', views.editAddress, name="editAddress"),
    path('deleteAddress/<int:id>/', views.deleteAddress, name="deleteAddress"),
    path('password_change', views.password_change, name="password_change"),
    path('activate-address', views.activate_address, name="activate-address"),
    path('addAddress', views.addAddress, name="addAddress"),

    
    path('otp_register', views.otp_register, name='otp_register'),
    path('logout',views.perform_logout, name='logout'),
    
    
]