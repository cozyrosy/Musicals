from calendar import month
from itertools import count
from urllib import request
from django.db.models import Sum,Count
from django.db.models.functions import ExtractMonth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm
from MyAdmin.helpers import save_pdf
from accounts.models import *
from category.models import *
from orders.models import *
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from orders.views import orders
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

import calendar
@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def adminHomee(request):
    print('ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
    
    if request.user.is_authenticated:
        orders = OrderProduct.objects.aggregate(Count('id')).get('id__count')
        users = Account.objects.aggregate(Count('id')).get('id__count')
        pdts = Product.objects.aggregate(Count('id')).get('id__count')
        cats = Category.objects.aggregate(Count('id')).get('id__count')
        order = Order.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month','count')
        monthNumber = []
        totalOrders = []
        for data in order:
            monthNumber.append(calendar.month_name[data['month']])
            totalOrders.append(data['count'])

        context = {
            'orders':orders,
            'users':users,
            'pdts':pdts,
            'cats':cats,
            'order':order,
            'monthNumber':monthNumber,
            'totalOrders':totalOrders
        }
        return render(request, 'adminHome.html',context)
    else:
        return redirect(adminLoginn)
   
@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def adminLoginn(request):
    print('llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll')
    if 'username' in request.session:
        return redirect(adminHomee)
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data= request.POST)
            if fm.is_valid():
                aname = fm.cleaned_data['username']
                apass = fm.cleaned_data['password']
                if aname == '':
                    messages.error(request, "enter ")
                admin = authenticate(username= aname, password= apass)
                # if aname == '':
                #     messages.error(request, 'Please enter the email')
                #     return render(request, 'adminLogin.html', {'form': fm})
                # if apass == '':
                #     messages.error(request, 'Please enter the password')
                #     return render(request, 'adminLogin.html', {'form': fm})
                if admin is not None:
                    if admin.is_admin:
                        login(request, admin)
                        return HttpResponseRedirect('/adminHome/adminHomee/')
        else:
            fm = AuthenticationForm()
        return render(request, 'adminLogin.html', {'form': fm})
    else:
        return redirect('adminHomee')

    
decorators = [never_cache,]

class adminUsersList(View):
    @method_decorator(decorators, name='dispatch')
    def get(self, request):
        user_data = Account.objects.all()
        # paginator= Paginator(user_data,3)
        # page_number= request.GET.get('page')
        # UserDataFinal = paginator.get_page(page_number)
        # totalpage=UserDataFinal.paginator.num_pages
        data =  {
            'userdata': user_data, 
            # 'totalPageList':[n+1 for n in range(totalpage)]
            }
        return render(request, 'adminUsersList.html', data)



class adminCategories(View):
    @method_decorator(decorators, name='dispatch')
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'adminCategories.html', {'category':categories})

@login_required(login_url='adminLogin')
class deleteCategory(View):
    def post(self, request):
        data = request.POST 
        name = data.get('name')
        catdata = Category.objects.get(name= name)
        catdata.delete()
        return redirect(adminCategories)

# PRODUCT MANAGEMENT

class adminProducts(LoginRequiredMixin, View):
    login_url = '/adminLogin/'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
        products = Product.objects.all()
        return render(request, 'adminProducts.html', {'product':products})

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def addProduct(request):    
    if request.user.is_authenticated:
        if request.method == "POST":
            pdt = Product()
            pdt.product_name = request.POST.get('name')
            pdt.product_image = request.POST.get('image')
            pdt.product_image_1 = request.POST.get('image1')
            pdt.product_image_2 = request.POST.get('image2')
            pdt.description = request.POST.get('description')
            pdt.quantity = request.POST.get('quantity')
            pdt.orignal_price = request.POST.get('price')
            pdt.tag = request.POST.get('tag')
            pdt.slug = request.POST.get('slug')
            category = request.POST.get('category')
            cat = Category.objects.get(id=category)
            pdt.category = cat
            filter_price = request.POST.get('filter_price')
            fp = PriceFilter.objects.get(id= filter_price)
            pdt.filter_price = fp
            if Product.objects.filter(product_name = pdt.product_name).exists():
                messages.error(request, 'Product already exists!!')
                return redirect('addProduct')
            if pdt.product_name == '':
                messages.error(request, 'Please enter the product name')
                return redirect('addProduct')
            if pdt.product_image == '':
                messages.error(request, 'Please enter the product image')
                return redirect('addProduct')
            if pdt.product_image_1 == '':
                messages.error(request, 'Please enter the product image')
                return redirect('addProduct')
            if pdt.product_image_2 == '':
                messages.error(request, 'Please enter the product image')
                return redirect('addProduct')
            if pdt.description == '':
                messages.error(request, 'Please enter the description')
                return redirect('addProduct')
            if pdt.quantity == '':
                messages.error(request, 'Please enter the quantity ')
                return redirect('addProduct')
            if pdt.tag == '':
                messages.error(request, 'Please enter the tag')
                return redirect('addProduct')
            if pdt.selling_price == '':
                messages.error(request, 'Please enter the category ')
                return redirect('addProduct')
            if category == '':
                messages.error(request, 'Please enter the category ')
                return redirect('addProduct')
            if len(request.FILES) != 0:
                pdt.product_image = request.FILES['image']
            pdt.save()
            messages.success(request,"Product added successfully")
            return redirect('adminProducts') 
        cat = Category.objects.all()
        fp = PriceFilter.objects.all()
        return render(request, 'addProduct.html', {'cat':cat, 'fp':fp})
    else:
        return redirect(adminLoginn)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def editProduct(request, pk):
    if request.user.is_authenticated:
        prod = Product.objects.get(id=pk)
        cat = Category.objects.all()
        fp = PriceFilter.objects.all()
        if request.method == 'POST':
            if len(request.FILES) != 0:
                if len(prod.product_image) > 0:
                    os.remove(prod.product_image.path)
                prod.product_image = request.FILES['image']
                prod.product_image_1 = request.FILES['image1']
                prod.product_image_2 = request.FILES['image2']
            prod.product_name = request.POST.get('name')
            prod.description = request.POST.get('description')
            prod.quantity = request.POST.get('quantity')
            prod.orignal_price = request.POST.get('price')
            prod.tag = request.POST.get('tag')
            prod.slug = request.POST.get('slug')
            category = request.POST.get('category')
            cat = Category.objects.get(id=category)
            prod.category = cat
            filter_price = request.POST.get('filter_price')
            fp = PriceFilter.objects.get(id= filter_price)
            prod.filter_price = fp
            prod.save()
            messages.success(request,"Product updated successfully")
            return redirect('adminProducts')
    else:
        return redirect(adminLoginn)


    context = {'prod':prod, 'cat':cat, 'fp':fp}
    return render(request, 'editProduct.html', context)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def deleteProduct(request,pk):
    if  request.user.is_authenticated:
        prod = Product.objects.get(id=pk)
        if len(prod.product_image) > 0:
            os.remove(prod.product_image.path)
        prod.delete()
        messages.success(request,"Product deleted successfully")
        return redirect('adminProducts')
    else:
        return redirect(adminLoginn)

# CATEGORY MANAGEMENT

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def editCategory(request, pk):
    if request.user.is_authenticated:
        cat = Category.objects.get(id=pk)
        if request.method == 'POST':
            if len(request.FILES) != 0:
                if len(cat.cat_image) > 0:
                    os.remove(cat.cat_image.path)
                cat.cat_image = request.FILES['image']
            cat.cat_name = request.POST.get('name')
            cat.description = request.POST.get('description')
            cat.slug = request.POST.get('slug')
            cat.save()
            messages.success(request,"Product updated successfully")
            return redirect('adminCategories')

        context = {'cat': cat}
        return render(request, 'editCategory.html', context)
    else:
        return redirect(adminLoginn)

@cache_control(no_cache =True, must_revalidate =True, no_store =True) 
@login_required(login_url='adminLogin')
def DeleteCategory(request, pk):
        if request.user.is_authenticated:
            cat = Category.objects.get(id=pk)
            if len(cat.cat_image) > 0:
                os.remove(cat.cat_image.path)
            cat.delete()
            messages.success(request,"Category deleted successfully")
            return redirect(request, 'adminCategories')
        else:
            return redirect(adminLoginn)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def addCategory(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            category = Category()
            category.category_name = request.POST.get('name')
            category.cat_image = request.POST.get('image')
            category.description = request.POST.get('description')
            category.slug = request.POST.get('slug')
            if Category.objects.filter(category_name = category.category_name).exists():
                messages.error(request, 'Category already exists!!')
                return redirect('addCategory')
            if category.category_name == '':
                messages.error(request, 'Please enter the category name')
                return redirect('addCategory')
            if category.cat_image == '':
                messages.error(request, 'Please enter the Category Image')
                return redirect('addCategory')
            if category.description == '':
                messages.error(request, 'Please enter the description')
                return redirect('addCategory')
            if len(request.FILES) != 0:
                category.cat_image = request.FILES['image']
            category.save()
            messages.success(request,"Category added successfully")
            return redirect('adminCategories')
        return render(request, 'addCategory.html')
    else:
        return redirect(adminLoginn)


@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def blockUser(request, pk):
    user = Account.objects.get(id = pk)
    if user.is_active:
        user.is_active = False
        messages.error(request,"User blocked successfully")
    else:
        user.is_active = True
        messages.error(request,"User unblocked successfully")
    user.save()
    
    return redirect('adminUsersList')
   
# ORDER MANAGEMENT
@login_required(login_url='adminLogin')
def adminOrders(request):
    orders = Order.objects.all()
    orderitems = OrderProduct.objects.all()
    outfor_delivery = Order.objects.filter(status = 'Out for delivery').aggregate(Count('id')).get('id__count')
    pending = Order.objects.filter(status = 'Pending').aggregate(Count('id')).get('id__count')
    delivered = Order.objects.filter(status = 'Delivered').aggregate(Count('id')).get('id__count')
       
    print(outfor_delivery)
    context={
        'orders':orders,
        'orderitems':orderitems,
        'outfor_delivery':outfor_delivery,
        'pending':pending,
        'delivered':delivered
    }
    return render(request,'adminOrders.html', context)

@login_required(login_url='adminLogin')
def order_status_view(request,id):
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    order = Order.objects.get(id=id)
    if request.method=='POST':
        status = request.POST.get('status')
        order.status = status
        print(order.status)
        order.save()
        messages.success(request,"Status updated successfully")
    return redirect(adminOrders)

@login_required(login_url='adminLogin')
def adminOrderDetails(request,id):
    print(id)
    orders = Order.objects.all()
    order= Order.objects.get(id=id)
    print("ffffffffffffffffffffffffffffffffffdsdsdfffffffffffffffffffffffffffffffffffffffffffffffffffff")
    print(order)
    orderitems = OrderProduct.objects.filter(order= order)
    for o in orderitems:
        print('lllllllllllllllllll')
        print(o.payment)
    print(orderitems)
    context = {
        'order':order,
        'orderitems': orderitems,
        'orders':orders
    }
    return render(request,'adminOrderDetails.html', context)

# DASHBOARD

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def dashboard(request):
    orders = Order.objects.all()
    # orderproduct = OrderProduct.objects.filter(product__category_name = 1)
    

    
    cod = Order.objects.filter(status = 'Out for delivery').aggregate(Count('id')).get('id__count')
       
    print(cod)
    


    return render(request, "adminindex.html", cod)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def salesReport(request):
    salesreport = OrderProduct.objects.all()
    #product_order = Product.objects.all()
    
    context = {
        'salesreport'   : salesreport,

        # 'product_order' : product_order
    }
    return render(request, 'salesreport.html', context)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def date_range(request):
    if request.method == "POST":
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        if len(fromdate)>0 and len(todate)> 0 :
            frm = fromdate.split("-")
            tod = todate.split("-")

            fm = [int(x) for x in frm]
            todt = [int(x) for x in tod]

            salesreport  = OrderProduct.objects.filter(created_at__gte = datetime.date(fm[0],fm[1],fm[2]),created_at__lte=datetime.date(todt[0],todt[1],todt[2]) )

            context = {
                'salesreport':salesreport 
            }

            return render(request,'salesreport.html',context)

        else:
            salesreport = OrderProduct.objects.all()
            context = {
                'salesreport': salesreport 

             }
    return render (request,"salesreport.html",context)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def monthly_report(request,date):
    frmdate = date
    fm = [2022, frmdate, 1]
    todt = [2022,frmdate,28]

    salesreport = OrderProduct.objects.filter(created_at__gte = datetime.date(fm[0],fm[1],fm[2]),created_at__lte=datetime.date(todt[0],todt[1],todt[2])).order_by("-id")
    if len(salesreport)>0:
        context = {
            'salesreport':salesreport,
        }
        return render(request,'salesreport.html',context)

    else:
        messages.error(request,"No Orders")
        return render(request,'salesreport.html')

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def yearly_report(request,date):
    frmdate = date
    fm = [frmdate, 1, 1]
    todt = [frmdate,12,31]

    salesreport = OrderProduct.objects.filter(created_at__gte = datetime.date(fm[0],fm[1],fm[2]),created_at__lte=datetime.date(todt[0],todt[1],todt[2])).order_by("-id")
    if len(salesreport)>0:
        context = {
            'salesreport':salesreport,
        }
        return render(request,'salesreport.html',context)

    else:
        messages.error(request,"No Orders")
        return render(request,'salesreport.html')


# COUPON MANAGEMENT

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def coupons(request):
    coupons = Coupon.objects.all()
    return render(request, 'adminCoupons.html', {'coupons':coupons})

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def addCoupon(request):
    if request.method=='POST':
        cpns = Coupon()
        cpns.coupon_code = request.POST.get('code')
        cpns.discount_price = request.POST.get('discount')
        cpnsoo = request.POST.get('checkk')
        if cpns.coupon_code == "":
            messages.success(request," Please enter the Coupon code!")
        if cpns.discount_price == "":
            messages.success(request," Please enter the offer!")
        try:
            discount=int(cpns.discount_price)
            if discount > 0 :
                if discount < 90: 
                    cpns.save()
                    print(type(cpnsoo))
                    return redirect(coupons)
                else:
                    messages.success(request," offer must be between 1% to 90%")
        except:
            messages.success(request," offer must be between 1% to 90%")
            return render(request, 'addCoupon.html')
       
    return render(request, 'addCoupon.html')

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')    
def couponBlock(request,pk):
    coupon_obj = Coupon.objects.get(id=pk)
    if coupon_obj.is_expired:
        coupon_obj.is_expired = False
        messages.error(request,"Coupon disabled successfully")
    else:
        coupon_obj.is_expired = True
        messages.error(request,"Coupon enabled successfully")
    coupon_obj.save()
    return redirect('adminCoupons')

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def couponDelete(request, pk):
    coupon_del = Coupon.objects.get(id=pk)
    coupon_del.delete()
    messages.success(request,"Coupon deleted successfully")
    return redirect(coupons)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def couponEdit(request,pk):
    cpn_edit = Coupon.objects.get(id=pk)
    # cpnss = Coupon.objects.al
    if request.method == 'POST':
        cpn_edit.coupon_code = request.POST.get('code')
        cpn_edit.discount_price = request.POST.get('discount')
        cpn_editss = request.POST.get('checkk')
        if cpn_edit.coupon_code == "":
            messages.success(request," Please enter the Coupon code!")
        if cpn_edit.discount_price == "":
            messages.success(request," Please enter the offer!")
        try:
            discount=int(cpn_edit.discount_price)
            if discount > 0 :
                if discount < 90: 
                    cpn_edit.save()
                
                    return redirect(coupons)
                else:
                    messages.success(request," offer must be between 1% to 90%")
        except:
            context = {'cpn_edit':cpn_edit}
            messages.success(request," offer must be between 1% to 90%")
            return render(request, 'couponEdit.html',context)
        
    context = {'cpn_edit':cpn_edit}
    return render(request, 'couponEdit.html',context)


# PRODUCT OFFER MANAGEMENT
@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def productOffer(request):
    prod_off = ProductOffer.objects.all()
    context = {
        'prod_off':prod_off
    }
    return render(request, 'productOffer.html', context)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def addProductOffer(request):
    prod = Product.objects.all()
    if request.method=='POST':
        prod_off = ProductOffer()
        cpnsoo = request.POST.get('check')
        prod_off.is_expired = cpnsoo
        prod_off.discount = request.POST.get('discount') 
        product = request.POST.get('product')
        cat = Product.objects.get(id=product)
        prod_off.product = cat
        if prod_off.discount == "":
            messages.success(request," Please enter the offer!")
        try:
            discount=int(prod_off.discount)
            if discount > 0 :
                if discount < 90: 
                    cat.discount_price = discount
                    cat.save()
                    prod_off.save()
                    return redirect(productOffer)
                else:
                    messages.success(request," offer must be between 1% to 90%")
        except:
            context={
            'prod':prod
            }
            messages.success(request," offer must be between 1% to 90%")
            return render(request, 'addProductOffer.html',context)
    
    context={
            'prod':prod
        }
    return render(request, 'addProductOffer.html',context)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def editProductOffer(request,pk):
    prod = Product.objects.all()
    prod_off_edit = ProductOffer.objects.get(id=pk)
    if request.method == 'POST':
        product = request.POST.get('product')
        prod_off_edit.discount = request.POST.get('discount')
        cat = Product.objects.get(id=product)
        # cpnsoo = request.POST.get('check')
        if prod_off_edit.discount == "":
            messages.success(request," Please enter the offer!")
        try:
            discount=int(prod_off_edit.discount)
            if discount > 0 :
                if discount < 90: 
                    cat.discount_price = discount
                    cat.save()
                    prod_off_edit.save()
                    return redirect(productOffer)
                else:
                    messages.success(request," offer must be between 1% to 90%")
        except:
            context={
            'prod':prod,
            'prod_off_edit':prod_off_edit
            }
            messages.success(request," offer must be between 1% to 90%")
            return render(request, 'editProductOffer.html',context)
          
        # print(type(cpnsoo))
       
    context={
            'prod':prod,
            'prod_off_edit':prod_off_edit
        }
    return render(request, 'editProductOffer.html',context)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def deleteProductOffer(request,pk):
    p_offer_del = ProductOffer.objects.get(id=pk)
    p_offer_del.delete()
    messages.success(request,"Product offer deleted successfully")
    return redirect(productOffer)

@login_required(login_url='adminLogin')
def productOfferBlock(request, pk):
    user = ProductOffer.objects.get(id = pk)
    if user.is_expired:
        user.is_expired = False
        messages.error(request,"Offer blocked successfully")
    else:
        user.is_expired = True
        messages.error(request,"Offer unblocked successfully")
    user.save()
    return redirect(productOffer)


# CATEGORY OFFER MANAGEMENT
@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def categoryOffer(request):
    cat_off = CategoryOffer.objects.all()
    context = {
        'cat_off':cat_off
    }
    return render(request, 'categoryOffer.html', context)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def addcategoryOffer(request):
    prod = Category.objects.all()
    if request.method=='POST':
        cat_off = CategoryOffer()
        category = request.POST.get('category')
        cat_off.discount_amnt = request.POST.get('discount')
        cpnsoo = request.POST.get('check')
        cat = Category.objects.get(id=category)
        cat_off.category = cat
        if cat_off.discount_amnt == "":
            messages.success(request," Please enter the offer!")
        try:
            discount=int(cat_off.discount_amnt)
            if discount > 0 :
                if discount < 90: 
                    cat.discount_amnt = cat_off.discount_amnt
                    cat.save()
                    cat_off.save()
                    print(type(cpnsoo))
                    return redirect(categoryOffer)
                else:
                    messages.success(request," offer must be between 1% to 90%")
        except:
            context={
            'prod':prod
            }
            messages.success(request," offer must be between 1% to 90%")
            return render(request, 'addcategoryOffer.html',context)
    
    context={
            'prod':prod
        }
    return render(request,'addcategoryOffer.html', context)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def editCategoryOffer(request,pk):
    prod = Category.objects.all()
    cat_off_edit = CategoryOffer.objects.get(id=pk)
    if request.method == 'POST':
        category = request.POST.get('product')
        cat_off_edit.discount_amnt = request.POST.get('discount')
        cpnsoo = request.POST.get('check')
        cat = Category.objects.get(id=category)
        cat_off_edit.category = cat
        if cat_off_edit.discount_amnt == "":
            messages.success(request," Please enter the offer!")

        try:
            discount=int(cat_off_edit.discount_amnt)
            if discount > 0 :
                if discount > 90: 
                    cat.discount_amnt = discount
                    cat.save()
                    cat_off_edit.save()
                    return redirect(productOffer)
                else:
                    messages.success(request," offer must be between 1% to 90%")
        except:
            context={
            'prod':prod,
            'prod_off_edit':cat_off_edit
            }
            messages.success(request," offer must be between 1% to 90%")
            return render(request, 'editCategoryOffer.html',context)
          
        cat_off_edit.save()
        print(type(cpnsoo))
        messages.success(request,'Offer updated successfully')
        return redirect(categoryOffer)   
    context={
            'prod':prod,
            'cat_off_edit':cat_off_edit
        }
    return render(request, 'editCategoryOffer.html',context )

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
@login_required(login_url='adminLogin')
def deleteCategoryOffer(request,pk):
    cat_offer_del = CategoryOffer.objects.get(id=pk)
    cat_offer_del.delete()
    messages.success(request,"Category offer deleted successfully")
    return redirect('categoryOffer')

@login_required(login_url='adminLogin')
def categoryOfferBlock(request, pk):
    user = CategoryOffer.objects.get(id = pk)
    if user.is_expired:
        user.is_expired = False
        messages.error(request,"Offer blocked successfully")
    else:
        user.is_expired = True
        messages.error(request,"Offer unblocked successfully")
    user.save()
    return redirect(categoryOffer)

