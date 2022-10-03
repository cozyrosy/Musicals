from hashlib import new
from multiprocessing import context
import re
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from .forms import *
from .models import Account,Profile,UserAddressBook
from category.models import Category, Product
from carts.models import *
from carts.views import _cart_id,checkout
from django.contrib import messages
import requests 
from django.conf import settings
from twilio.rest import Client
from django.contrib.auth.models import auth


# Create your views here.
@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def home(request):
    # if request.user.is_authenticated:
        category = Category.objects.all()
        cat_off = CategoryOffer.objects.all()
        product = Product.objects.filter( tag = 'Featured').order_by('-id')
        new = Product.objects.filter(tag='New').order_by('-id')
        context = {
            'category':category,
            'product':product,
            'new': new,
            'cat_off':cat_off
            }
        return render(request, "home.html", context)
    # else:
        # return redirect('login')
decorators = [never_cache,]

class registerView(View):
    def get(self, request):
        reg_form = RegisterForm()
        return render(request, 'register.html', {'form':reg_form})
    def post(self, request):
        reg_form = RegisterForm(request.POST)
       
        if reg_form.is_valid():
            
            phone_number = reg_form.cleaned_data['phone_number']
            print(phone_number)
            print(type(phone_number))
            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

            phone_num = "+91" + str(phone_number)
            print('//////////////////////////////////////////////////////////////////')
            print(type(phone_num))
            print('//////////////////////////////////////////////////////////////////')
            
            reg_form.save() 
            # username= reg_form.cleaned_data['email']

            account_sid = settings.ACCOUNT_SID
            auth_token = settings.TOKEN_SID
            client = Client(account_sid,auth_token)
            verification = client.verify \
                    .services(settings.SERVICES) \
                    .verifications \
                    .create(to=phone_num ,channel='sms')
            
            return render(request,'otp_login.html',{'phone_number':phone_number })

            
            # return redirect('login')
        else:
            messages.error(request, 'Please enter the valid data')
            return render(request, 'register.html', {'form':reg_form})


def otpentersignup(request,phone_number):
    username = request.GET.get('username')
    phone_no = "+91" + str(phone_number)


    if request.method == 'POST':
        
            
            otp_input   = request.POST.get('enterotp')

            if len(otp_input)>3:
                account_sid = settings.ACCOUNT_SID
                auth_token = settings.TOKEN_SID
                client = Client(account_sid, auth_token)
            
                verification_check = client.verify \
                                    .services(settings.SERVICES) \
                                    .verification_checks \
                                    .create(to= phone_no, code= otp_input)

                if verification_check.status == "approved":
                    # traluser = trial.objects.get(username =username)
                    user = Account.objects.get(phone_number=phone_number)
                    user.phone_number = phone_number
                    user.save()
                    # traluser.delete()
                    auth.login(request,user)
                    return redirect('home')
                else:
                    # messages.error(request,'Invalid OTP')
                    # return render(request,'otpverification.html',{'phone_number':phone_number ,'username':username})

                    return redirect('otplogin.html',{'phone_number':phone_number })
            else:
                return redirect('otplogin.html',{'phone_number':phone_number })

    else:
        return render(request,'otp_login.html',{'phone_number':phone_number})


def otpLogin(request):
    if request.method == 'POST':
        phone_number = request.POST.get('enterphone')
        phone_no = "+91" + str(phone_number)

        
        if Account.objects.filter(phone_number=phone_number).exists():
            user = Account.objects.get(phone_number = phone_number)
            print(user)
            print(phone_number)
            print('///////////////////////////////////////////////////////////////////////////////////////////')
            account_sid = settings.ACCOUNT_SID
            auth_token = settings.TOKEN_SID
            client = Client(account_sid,auth_token)
            verification = client.verify \
                .services(settings.SERVICES) \
                .verifications \
                .create(to=phone_no ,channel='sms')
            
            return render(request,'otp_loginenter.html',{'phone_number':phone_number})

        else:
            # messages.info(request,'invalid Mobile number')
            return redirect(otpLogin)
    print('outsidwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
    return render(request, 'otp_userlogin.html')


def otpenterlogin(request,phone_number ):
    if request.method == 'POST':
        if Account.objects.filter(phone_number=phone_number):
            user      = Account.objects.get(phone_number=phone_number)
            phone_no = "+91" + str(phone_number)
            otp_input   = request.POST.get('otp')
            
            if otp_input=='':
                messages.error(request,'Invalid OTP')
            elif int(otp_input) <=3:
                messages.error(request,'Invalid OTP')
            if len(otp_input)>3:
                account_sid = settings.ACCOUNT_SID
                auth_token = settings.TOKEN_SID
                client = Client(account_sid, auth_token)
            
                verification_check = client.verify \
                                    .services(settings.SERVICES) \
                                    .verification_checks \
                                    .create(to= phone_no, code= otp_input)

                if verification_check.status == "approved":
                    auth.login(request,user)
                    return redirect(home)
                else:
                    messages.error(request,'Invalid OTP')
                    return render(request,'otp_loginenter.html',{'phone_number':phone_number})

                   

            else:
                messages.error(request,'Invalid OTP')
                return render(request,'otp_loginenter.html',{'phone_number':phone_number})

        else:

            messages.error(request,'Invalid Phone number')
            return redirect('otpLogin')
    return render(request, 'otp_loginenter.html')


class loginView(View):
    @method_decorator(decorators,name='dispatch')
    def get(self, request):
        if 'username' in request.session:
            return redirect(home)
        else:
            fm = AuthenticationForm()
            return render(request, 'login.html', {'form':fm} )
    
    def post(self, request):
       
            fm = AuthenticationForm(request, data=request.POST)
            
            if fm.is_valid():
                username = fm.cleaned_data['username']
                password = fm.cleaned_data['password']

                if username == "":
                    messages.error(request, 'Please enter a valid data')
                    return render(request, 'login.html', {'form': fm})

                user = authenticate( username=username, password=password)
                if user is not None:
                    try:
                        cart = Cart.objects.get(cart_id = _cart_id(request))
                        cart_item = cartItem.objects.filter(cart = cart)
                        user_cart = cartItem.objects.filter(user = user)
                        
                        for x in cart_item:
                            a=0
                            for y in user_cart:
                                if x.product == y.product:
                                    y.quantity += x.quantity 
                                    y.save()
                                    x.delete()
                                    a=1
                                    break
                            if a==0:
                                x.user=user
                                x.save()
                    except:
                        pass
                    request.session['username']=username
                    print('valid')
                    login(request,user)         
                    url = request.META.get('HTTP_REFERER')
                    try:
                        query= requests.utils.urlparse(url).query
                        #next=cart/checkout
                        params = dict(x.split('=') for x in query.split('&'))
                        if 'next' in params:
                            nextPage = params['next']
                            return redirect(nextPage)
                    except:
                        return redirect('home')
                else:
                    print('asdfsdf')
                    messages.error(request, 'Please enter a valid data')
                    return render(request, 'login.html', {'form': fm})
            else:
                print('invalid')
                messages.error(request, 'Please enter a valid data')
                return render(request, 'login.html', {'form': fm})
       
def perform_logout(request):
    if 'username' in request.session:
        user = request.user
        logout(request)
        request.session.flush()
    return redirect(home)


def collectionView(request, slug):
    print('hhhhhhhhhhhhhh')
    c_offer=0
    try:
        if(Category.objects.get(slug=slug)):
            products = Product.objects.filter(category__slug=slug)
            prod = ProductOffer.discount
            category_name = Category.objects.filter(slug=slug).first()
            cat = Category.objects.get(slug=slug)
            filter_price = PriceFilter.objects.all()
            category = Category.objects.all()
        
            print('ppppppppppppppppppppppppp')
            try:
                print('//////////////')
                
                PRICE_FILTER_ID = request.GET['filter_price']
                print(PRICE_FILTER_ID)
                
                if PRICE_FILTER_ID:
                    print('........................',PRICE_FILTER_ID)
                    products = Product.objects.filter(filter_pricee = PRICE_FILTER_ID) 
                else:
                    products = Product.objects.filter(category__slug=slug)
            except:
                pass
            try:
                CAT_ID   = request.GET['categories']
                if CAT_ID:
                    products = Product.objects.filter(category__slug=CAT_ID)
                else:
                    products = Product.objects.filter(category__slug=slug)
            except:
                pass
            
            try:
                cat_offer = CategoryOffer.objects.get(category=cat)
                c_offer = cat_offer.discount_amnt
                # print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh, ', cat_offer.category.category_name)
                # print('fffffffffffffffffffffffffffffffffff', cat_offer.discount_amnt)
            except:
                pass
            
            for p in products:
                try:
                    prod_offer = ProductOffer.objects.get(product__id=p.id)
                    p_offer = prod_offer.discount
                    print('lllllllllllllllllllllllllllll',p_offer, 'rrrrrr', prod_offer)
                    if p_offer:
                        print('offfffff',p.discount_price)
                        p.discount_price = int( p.orignal_price - ( p.orignal_price * ( p_offer / 100 )))
                        print('dissssssss',p.discount_price)
                        p.save()
                    if c_offer :
                        p.discount_price = int( p.orignal_price - ( p.orignal_price * ( c_offer / 100 )))
                        print('diiiii',p.discount_price)
                        p.save()      
                except:
                    # if not p_offer :
                    #     p.discount_price = None
                    #     p.save()
                    if c_offer :
                        p.discount_price = int( p.orignal_price - ( p.orignal_price * ( c_offer / 100 )))
                        print('aaaaaaaa',p.discount_price)
                        p.save()
                    else:
                        p.discount_price = 0
                        p.save()
                
            
                try:
                    if ProductOffer.objects.get(product__id=p.id) and CategoryOffer.objects.get(category=cat):
                        # print('proddddddd', prod_offer)
                        # print('proddddddd222', p_offer)
                        # print('catttttttt', cat_offer)
                        # print('catttttttt222', c_offer)
                        if p_offer > c_offer:
                            p.discount_price = int( p.orignal_price - ( p.orignal_price * ( p_offer / 100 )))
                            print('bbbbbbbbbb',p_offer, p.discount_price)
                            p.save()
                        else:
                            p.discount_price = int( p.orignal_price - ( p.orignal_price * ( c_offer / 100 )))
                            print('cccccccccc',c_offer, p.discount_price)
                            p.save()
                except:
                    print('qwert')
            
                
            context = {
                'products': products,
                'category_name':category_name,
                'prod':prod,
                'filter_price':filter_price,
                'category':category
                }
            return render(request,'products.html', context)
        else:
            # messages.warning(request,"No such category found")
            return redirect('home')
    except:
        pass
        # return redirect('home')

def productView(request, cat_slug, prod_slug):

    if(Category.objects.filter(slug=cat_slug)):
        if(Product.objects.filter(slug=prod_slug)):
            products = Product.objects.filter(slug=prod_slug).first()
           
            context = {
                'products': products,
                
            }
            prod= Product.objects.all()
            # b = CategoryOffer.objects.get(category =prod.id)
            # cp = b.discount_amnt
            # for pro in prod :
            #     a = ProductOffer.objects.get(product =pro.id)
            #     pp = a.discount
            #     if pro.category.discount_amnt:
            #         if pro.discount_price:
            #             if pp > cp:
            #                 pro.discount_price = pp
            #             else:

                        

        else:
            # messages.error(request,"No such product found")
            return redirect('home')
    else:
        # messages.error(request,"No such category found")
        return redirect('home')
        
    return render(request, 'productdetails.html', context)

def otp_register(request):
    return render(request,'otp_login.html')

def userProfile(request):
    return render(request, 'userProfile.html')

# My Address Book 
def my_addressbook(request):
    addbook = UserAddressBook.objects.filter(user=request.user).order_by('-id')
    return render(request, 'my_addressbook.html', {'addbook': addbook})

# Save AddressBook
def save_address(request):
    msg = None
    if request.method == 'POST':
        form = AddressBookForm(request.POST)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            saveForm.save()
            msg = 'Your data has been saved '
    form = AddressBookForm 
    return render(request, 'save_address.html', {'form': form, 'msg':msg})

def activate_address(request):
    a_id=str(request.GET['id'])
    UserAddressBook.objects.update(status=False)
    UserAddressBook.objects.filter(id=a_id).update(status=True)
    # data={'bool'}
    return JsonResponse({'bool':True})

def editProfile(request):
    msg =None
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            msg = 'Your data has been saved '
    form = ProfileForm(instance=request.user)
    return render(request, 'editProfile.html', {'form': form, 'msg': msg})

def editAddress(request, id):
    address = UserAddressBook.objects.get(pk=id)
    msg = None
    if request.method == 'POST':
        form = AddressBookForm(request.POST, instance=address)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            saveForm.save()
            msg = 'Your data has been saved '
    form = AddressBookForm(instance=address)
    return render(request, 'editAddress.html', {'form': form, 'msg':msg})

def deleteAddress(request, id):
    del_address = UserAddressBook.objects.get(pk=id)
    del_address.delete()
    messages.success(request,"Category offer deleted successfully")
    return redirect(my_addressbook)

def password_change(request):
    context = {}
    if request.method == "POST":
        current = request.POST["cpwd"] 
        new_pass = request.POST["npwd"]
        
        user = Account.objects.get(id = request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
            user.set_password(new_pass)
            user.save()
            context["msg"] = "Password Changed Successfully !"
            context["col"] = "alert-success"
            user = Account.objects.get(username = un)
            login(request, user)
        else:
            context["msg"] = "Current Password is Incorrect !"
            context["col"] = "alert-danger"
    print('mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
    return render(request, 'password_change_form.html', context )

def addAddress(request):    
    msg = None
    if request.method == 'POST':
        form = AddressBookForm(request.POST)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            saveForm.save()
            msg = 'Your data has been saved'
            return redirect(checkout)
    form = AddressBookForm 
    return render(request, 'addAddress1.html',  {'form': form, 'msg':msg})