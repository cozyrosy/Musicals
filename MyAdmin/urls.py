from django.urls import path 
from . import views
from django.views.generic import View
from django.contrib.auth.views import LogoutView

urlpatterns = [
# ADMIN ACCESS
    path('adminLogin/',views.adminLoginn, name='adminLogin'),
    path('adminHomee/', views.adminHomee, name="adminHomee"),  
# ADMIN DASHBOARD
    path('salesReport/', views.salesReport, name="salesReport"),
    path("monthly_report/<int:date>/",views.monthly_report,name="monthly_report"),
    path("yearly_report/<int:date>/",views.yearly_report,name="yearly_report"),
    path("date_range/",views.date_range,name="date_range"),
    
# ADMIN USER MANAGEMENT 
    path('adminUsersList/', views.adminUsersList.as_view(), name= "adminUsersList"),
    path('blockUser/<str:pk>', views.blockUser, name= "blockUser"),
# ADMIN CATEGORY MANAGEMENT
    path('adminCategories/', views.adminCategories.as_view(), name= "adminCategories"),
    path('editCategory/<str:pk>', views.editCategory, name='editCategory'),
    path('DeleteCategory/<str:pk>', views.DeleteCategory, name= "DeleteCategory"),
    path('addCategory/', views.addCategory, name='addCategory'),
# ADMIN PRODUCT MANAGEMENT
    path('adminProducts/', views.adminProducts.as_view(), name= "adminProducts"),
    path('addProduct/', views.addProduct, name='addProduct'),
    path('editProduct/<str:pk>', views.editProduct, name='editProduct'),
    path('deleteProduct/<str:pk>', views.deleteProduct, name='deleteProduct'),

# ADMIN ORDER MANAGEMENT
    path('adminOrders/', views.adminOrders, name="adminOrders"),
    path('orderStatusView/<str:id>/', views.order_status_view, name="order_status_view"),
    path('adminOrderDetails/<int:id>', views.adminOrderDetails, name='adminOrderDetails'),
# ADMIN COUPON MANAGEMENT 
    path('adminCoupons/', views.coupons, name="adminCoupons"),
    path('addCoupon/', views.addCoupon, name="addCoupon"),
    path('couponBlock/<str:pk>', views.couponBlock, name="couponBlock"),
    path('couponDelete/<str:pk>', views.couponDelete, name="couponDelete"),
    path('couponEdit/<str:pk>', views.couponEdit, name="couponEdit"),
# ADMIN PRODUCT OFFER MANAGEMENT
    path('productOffer/', views.productOffer, name="productOffer"),
    path('addProductOffer/', views.addProductOffer, name="addProductOffer"),
    path('editProductOffer/<str:pk>', views.editProductOffer, name="editProductOffer"),
    path('deleteProductOffer/<str:pk>', views.deleteProductOffer, name="deleteProductOffer"),
    path('productOfferBlock/<str:pk>', views.productOfferBlock, name='productOfferBlock'),
# ADMIN CATEGORY OFFER MANAGEMENT
    path('categoryOffer/', views.categoryOffer, name="categoryOffer"),
    path('addcategoryOffer/', views.addcategoryOffer, name="addcategoryOffer"),
    path('editCategoryOffer/<str:pk>', views.editCategoryOffer, name="editCategoryOffer"),
    path('deleteCategoryOffer/<str:pk>', views.deleteCategoryOffer, name="deleteCategoryOffer"),
    path('categoryOfferBlock/<str:pk>', views.categoryOfferBlock, name="categoryOfferBlock"),
# ADMIN LOGOUT
    path('adminLogout/',LogoutView.as_view(next_page= 'adminLogin'), name='adminLogout'),
    
]