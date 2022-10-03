
import json
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from carts.models import cartItem
from accounts.views import *
from carts.views import checkout, checkOffer, checkCoupon
from orders.forms import *
from orders.models import Order, OrderProduct
from django.contrib.auth.decorators import login_required
from accounts.views import home
import random
import razorpay
from firstEcom.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY

# Create your views here.



def place_order(request):
    # addid=addid
    total = 0
    if request.method == 'POST':
        neworder = Order()
        neworder.user= request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.phone = request.POST.get('phone')
        neworder.email = request.POST.get('email')
        neworder.address = request.POST.get('address')
        neworder.country = request.POST.get('country')
        neworder.state = request.POST.get('state')
        neworder.city = request.POST.get('city')
        neworder.pincode = request.POST.get('pincode')
        neworder.payment_mode = request.POST.get('payment_mode')
        print(neworder.payment_mode,'pasasa')
        neworder.payment_id = request.POST.get('payment_id')
        print(neworder.payment_id,'pasasa')

        cart = cartItem.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            print('gggggggggggg', item.product)
            neworder.product = item.product
            total += checkOffer(item) * item.quantity
            
            # cart_total_price = cart_total_price + item.product.orignal_price * item.quantity
        tax = (1*total)/100
        total = total + tax
        print('uuuuuuuuuu', total)
        trackno= 'rose' +str(random.randint(1111111,9999999))
        # neworder.product = product
        while Order.objects.filter(tracking_no = trackno) is None:
            trackno= 'rose' +str(random.randint(1111111,9999999))
        neworder.tracking_no= trackno
        neworder.total_price = total
        print('nnnnnnnnn', neworder.total_price)
        neworder.save()

        neworderitems = cartItem.objects.filter(user=request.user)
        for item in neworderitems:
            OrderProduct.objects.create(
                user= request.user,
                order=neworder,
                product= item.product,
                product_price = item.product.orignal_price,
                quantity = item.quantity
            )
            
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.quantity
            orderproduct.save()
        #to clear user's cart
        cartItem.objects.filter(user=request.user).delete()

        neworder.payment_mode = request.POST.get('payment_mode')
        
        if (neworder.payment_mode == "Paypal"):
            print('??????????', neworder.payment_mode)
            return JsonResponse({'status':"Your order has placed successfully"})
        else:
            messages.success(request,"Your order has placed successfully")
            

        if 'coupon_code' in request.session:
            del request.session['coupon_code']

    return redirect (order_invoice)

def orders(request,total=0, quantity=0, cart_items=None):
    order = Order.objects.filter(user = request.user ).order_by('-id')
    # p = Paginator(order,9)
    # page = request.GET.get('page')
    # orders = p.get_page(page)

    try:
        cart_items  = cartItem.objects.filter(user = request.user, is_active = True)
      

        for cart_item in cart_items:
            
            total += (cart_item.product.selling_price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (1*total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
    'total':total,
    'quantity':quantity,
    'cart_items':cart_items,
    'tax':tax,
    'grand_total':grand_total,
    'orders':order,
    }
  
    return render(request, 'orders.html',context)
            

# def orderView(request, t_no, total=0, quantity=0, cart_items=None):
    
#     tax=0
#     grand_total=0
#     print('dddddddddddddddddddddddddddd')

#     try:
#         order= Order.objects.filter(tracking_no= t_no).filter(user=request.user).first()
#         orderitems = OrderProduct.objects.filter(order= order)
#         cart_items  = cartItem.objects.filter(user = request.user, is_active = True)
            
#         for cart_item in cart_items:
#             print(cart_item.product.selling_price)
#             total += cart_item.product.selling_price * cart_item.quantity
#             quantity += cart_item.quantity
#         tax = (1*total)/100
#         grand_total = total + tax
#     except ObjectDoesNotExist:
#         pass
#     context = {
#         'order':order,
#         'orderitems': orderitems,
#         'total':total,
#         'quantity':quantity,
#         'cart_items':cart_items,
#         'tax':tax,
#         'grand_total':grand_total,
#     }
#     return render(request,'orderView.html', context)

def orderView(request, id):
    order = Order.objects.get(id=id)
    prod =OrderProduct.objects.filter(order = order)
    # total =0
    # quantity=0
    # grand_total = 0
    # try:
    #     cart_items  = cartItem.objects.filter(user = request.user, is_active = True)
    #     for cart_item in cart_items:
    #             total += checkOffer(cart_item) * cart_item.quantity
    #             print('111111111111111111sss', total)
    #             print( cart_item.product.orignal_price)
    #             quantity += cart_item.quantity
    #     tax = (1*total)/100
    #     print('111111111111111111', total)
        
    #     grand_total = checkCoupon(request,total) + tax
       
    #     order_amount= int(grand_total)
    #     print(total)
    #     print(order_amount)
    # except:
    #     pass
    context = {
        'order':order,
        'prod' : prod,
        # 'order_amount':order_amount
    }
    return render(request, 'orderView.html', context )

def orderComplete(request):
        total = 0
        address = UserAddressBook.objects.get(id=addid)
        neworder = Order()
        neworder.user= request.user
        neworder.lname = address.lname
        neworder.phone = address.phone
        neworder.address = address.address
        neworder.country = address.country
        neworder.state = address.state
        neworder.city = address.city
        neworder.pincode = address.pincode
        neworder.payment_mode = 'Razorpay'
       
        
        cart = cartItem.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            print('gggggggggggg', item.product)
            neworder.product = item.product
            total += checkOffer(item) * item.quantity
        trackno= 'rose' +str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no = trackno) is None:
            trackno= 'rose' +str(random.randint(1111111,9999999))
        tax = (1*total)/100
        total = total + tax
        print('uuuuuuuuuu', total)  
        neworder.tracking_no= trackno
        neworder.total_price = total
        neworder.save()

        neworderitems = cartItem.objects.filter(user=request.user)
        for item in neworderitems:
            OrderProduct.objects.create(
                user= request.user,
                order=neworder,
                product= item.product,
                product_price = item.product.orignal_price,
                quantity = item.quantity
            )
            
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.quantity
            orderproduct.save()
        #to clear user's cart
        cartItem.objects.filter(user=request.user).delete()
        if 'coupon_code' in request.session:
            del request.session['coupon_code']
        return redirect(    order_invoice)

def orderCancel(request,id):
    print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
    print(request.user)
    order = Order.objects.get(id=id)
    product = OrderProduct.objects.filter(order=order)
    for op in product:
        p=Product.objects.get(id=op.product.id)
        p.quantity = op.product.quantity + op.quantity
        print(p.quantity)
        
        p.save()
        print(p.quantity)
    order.status = 'Cancelled'
    order.save()

    # product.quantity +=order.quantity
    

    return redirect(orderView,id)
    
def orderReturn(request,id):
    print(request.user)
    order = Order.objects.get(id=id)
    product = OrderProduct.objects.filter(order=order)
    for op in product:
        p=Product.objects.get(id=op.product.id)
        p.quantity = op.product.quantity + op.quantity
        print(p.quantity)
        
        p.save()
        print(p.quantity)
    order.status = 'Returned'
    order.save()

    return redirect(orderView,id)

def payPal(request):
    body = json.loads(request,body)
    print('jjjj')
    print(body)
    return render()

def paymentMethod(request):
    total =0
    quantity=0
    grand_total = 0
    payment_order_id = 0
    cart_items=None
    if request.method == 'POST':
        global addid
        addid = request.POST.get('addid')
    try:
        address = UserAddressBook.objects.get(id=addid)
    except:
        messages.error(request, 'Choose an address to make payment')
        return redirect()
    client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
    try:
        cart_items  = cartItem.objects.filter(user = request.user, is_active = True)
        for cart_item in cart_items:
                total += checkOffer(cart_item) * cart_item.quantity
                print( cart_item.product.orignal_price)
                quantity += cart_item.quantity
        tax = (1*total)/100
        print('111111111111111111', total)
        
        grand_total = checkCoupon(request,total) + tax
       
        order_amount= int(grand_total)
        print(total)
        print(order_amount)
        print('444444444444444444444444444444444444444444')
        
        order_currency= "INR"
        payment_order = client.order.create(dict(amount=order_amount*100,currency=order_currency, payment_capture=1))
        payment_order_id = payment_order['id']
    except ObjectDoesNotExist:
            pass
    context = {
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'amount':grand_total,
        'api_key':RAZORPAY_API_KEY,
        'address': address,
        'order_id':payment_order_id,
        'total':total
    }
    return render(request, 'payment.html',context)

    # return render(request, 'payment.html', context)

def order_invoice(request):
    
    return render(request, 'orderComplete.html')