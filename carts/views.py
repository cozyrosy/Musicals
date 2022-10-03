
from urllib import request
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import UserAddressBook
from carts.models import Cart, cartItem
from django.core.exceptions import ObjectDoesNotExist
from category.models import Coupon, Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def checkOffer(cart_item):
    if cart_item.product.discount_price:
        print('llllllllll',cart_item.product.discount_price)
        total =  cart_item.product.discount_price
        print('jjjjjjj', total)
    else:
        print('pppppppppppppppppppppppppppppppppp')
        total = cart_item.product.orignal_price
    return total


def checkCoupon(request,total):
    print('sssssss', total)
    if 'coupon_code' in request.session:
        coupon= request.session['coupon_code']
        print('pppppppppp')
        coupons = Coupon.objects.get(coupon_code = coupon )
        coupon_off = coupons.discount_price
        print('ooooooo', total)
        total = int(total -(total * (coupon_off/100)))
    else:
        total = total
    return total

def add_cart(request,product_id, total=0, quantity=0):

    product = Product.objects.get(id=product_id) #get the product
    print(product)
    if request.user.is_authenticated:
        try:
            cart_items = cartItem.objects.get(product=product, user=request.user)
            print(cart_items)
            if cart_items:
                # cart_items.delete()
                cart_items.quantity += 1
                cart_items.save()

        except cartItem.DoesNotExist:
            cart_items = cartItem.objects.create(product= product, user = request.user, quantity =1)  
            print('asdf asdfsadfsdfsdfsdfsadfasdfsadhkjhitg;kjhkg;kfgjbkm,bgkurufgvkjmvnmdcyujgbkj')

            cart_items.save()
    else:
        
        try: 
            cart = Cart.objects.get(cart_id= _cart_id(request)) # get the cart using the cart_id
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        try :
            cart_item = cartItem.objects.get(product= product, cart=cart)
            cart_item.quantity +=1
            cart_item.save()
        except cartItem.DoesNotExist:
            cart_item = cartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            cart_item.save()
    return redirect(cartview)

def remove_cart(request, product_id):
    product=Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        cart_item = cartItem.objects.get(product=product, user= request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
    else:
        cart = Cart.objects.get(cart_id= _cart_id(request))
        product = get_object_or_404(Product, id= product_id)
        cart_item = cartItem.objects.get(product=product, cart= cart)
        if cart_item.quantity > 1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, product_id):
    product=Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        cart_item = cartItem.objects.get(product=product, user= request.user)

    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id= product_id)
        cart_item = cartItem.objects.get(product=product, cart= cart)
    cart_item.delete()
    return redirect('cart')

def cartview(request, total=0, quantity=0, cart_items=None):
    tax=0
    grand_total=0
    
    if request.user.is_authenticated:
        try:
            cart_items  = cartItem.objects.filter(user = request.user, is_active = True)
            for cart_item in cart_items:
                print(cart_item.product.orignal_price)
                total += checkOffer(cart_item) * cart_item.quantity
                print("------------------------------------------------------------------------------------------------------")
                print(total)
                print(type(checkOffer(cart_item)))
                print("*****************************************************************")
               
                quantity += cart_item.quantity
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            
            tax = (1*total)/100
            grand_total = total + tax    
            if request.method == 'POST':
                
                coupon = request.POST.get('coupon')
                request.session['coupon_code'] = coupon
                cart_obj  = cartItem.objects.filter(user = request.user)
                print('rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
                coupon_obj = Coupon.objects.filter(coupon_code__icontains=coupon)
                if not coupon_obj.exists():
                    print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
                    messages.warning(request, 'Invalid Coupon')
                    return redirect(cartview)
                if cart_obj[0].coupon:
                    messages.warning(request, 'Coupon already exists')
                    return render(request, 'cart.html')

                cart_obj[0].coupon = coupon_obj[0]
                cart_obj[0].save()
                
                    # print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
                coupon = Coupon.objects.get(coupon_code = request.session['coupon_code'])
                coupon_discount = coupon.discount_price
                reduction = total -(total * (coupon_discount/100))
                tax = (1*total)/100
                grand_total = total + tax - reduction
               
                messages.success(request, 'Coupon applied successfully')
                context = {
                        'total':total,
                        'quantity':quantity,
                        'cart_items':cart_items,
                        'tax':tax,
                        'grand_total':grand_total, 
                        'coupon':coupon_discount,
                        'coupon_code':coupon  
                        }

                return render(request, 'cart.html',context)

                  
        except ObjectDoesNotExist:
            pass
        context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,        
        }

    else:
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items =cartItem.objects.filter(cart= cart, is_active= True)
            for cart_item in cart_items:
                total += cart_item.product.orignal_price * cart_item.quantity
                quantity += cart_item.quantity
            tax = (1*total)/100
            grand_total = total + tax
            
        except ObjectDoesNotExist:
            pass
        context = {
            'total' : total,
            'quantity' : quantity,
            'cart_items' : cart_items,
            'tax' : tax,
            'grand_total' : grand_total,
        }
    return render(request, 'cart.html', context)


def updatecart(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if(cartItem.objects.filter(user=request.user, product_id = prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart_items = cartItem.objects.get(product_id=prod_id, user=request.user)
            cart_items.quantity = prod_qty
            cart_items.save()
            
            print(cart_items)
            return JsonResponse({'status':"Updated Successfully"}) 
    return redirect(cartview)


@login_required(login_url='login')
def checkout(request,total=0, quantity=0, cart_items=None):
    tax=0
    grand_total=0
    if request.user.is_authenticated:
        try:
            cart_items  = cartItem.objects.filter(user = request.user, is_active = True)
            
            for cart_item in cart_items:
            
                total += checkOffer(cart_item) * cart_item.quantity
                quantity += cart_item.quantity
            tax = (1*total)/100
            print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            print(total)
            grand_total = total + tax
            address = UserAddressBook.objects.filter(user=request.user) 
        except ObjectDoesNotExist:
            pass
            
        context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'address':address,
        }

    else:
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items =cartItem.objects.filter(cart= cart, is_active= True)
            for cart_item in cart_items:
                total += (cart_item.product.orignal_price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (1*total)/100
            grand_total = total + tax
            address = UserAddressBook.objects.filter(user=request.user) 
        except ObjectDoesNotExist:
            pass
        context = {
            'total' : total,
            'quantity' : quantity,
            'cart_items' : cart_items,
            'tax' : tax,
            'grand_total' : grand_total,
            'address':address,
        }
    
    return render(request, 'checkout.html', context)
