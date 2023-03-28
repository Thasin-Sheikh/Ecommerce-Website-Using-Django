from itertools import product
from os import stat
from unicodedata import category
from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required,name='dispatch')
class ProductView(View):
    def get(self,request):
        totalitem=0
        laptop=Product.objects.filter(category='L')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        camera=Product.objects.filter(category='C')
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/home.html',{'laptop':laptop, 'bottomwears':bottomwears,'mobiles':mobiles,'camera':camera,'totalitem':totalitem})

#def product_detail(request):
 #return render(request, 'app/productdetail.html')
@method_decorator(login_required,name='dispatch')
class ProductDetailView(View):
    def get(self,request,pk):
        totalitem=0
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
              totalitem=len(Cart.objects.filter(user=request.user))
              item_already_in_cart=Cart.objects.filter(Q(product=product.id)& Q(user=request.user)).exists()
        return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})

@login_required
def add_to_cart(request):
    
    user=request.user
    product_id = request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def plus_cart(request):
    totalitem=0
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=50.0
        cart_product=[p for p in Cart.objects.all() if p.user== request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount
            
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
            }
        return JsonResponse(data)

@login_required
def minus_cart(request):
    totalitem=0
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=50.0
        cart_product=[p for p in Cart.objects.all() if p.user== request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount
           
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
            }
        return JsonResponse(data)
@login_required
def remove_cart(request):
    totalitem=0
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=50.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount
        data={
            
            'amount':amount,
            'totalamount':amount+shipping_amount
            }
        return JsonResponse(data)

@login_required
def show_cart(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=50.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user== user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discounted_price)
                amount+=tempamount
                totalamount=amount+shipping_amount
            return render(request, 'app/addtocart.html',{'carts': cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem})
        else:
            return render(request,'app/emptycart.html',{'totalitem':totalitem})

@login_required
def buy_now(request):
 totalitem=0
 return render(request, 'app/buynow.html')

#def profile(request):
 #return render(request, 'app/profile.html')
@login_required
def address(request):
    totalitem=0
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-success'})

@login_required
def orders(request):

    op=OrderPlaced.objects.filter(user=request.user)
    totalitem=0
    if request.user.is_authenticated:
              totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html',{
        'order_placed':op,'totalitem':totalitem})


@login_required
def mobile(request,data=None):
    totalitem=0
    if request.user.is_authenticated:
              totalitem=len(Cart.objects.filter(user=request.user))
    if data == None:
        mobiles=Product.objects.filter(category='M')
    elif data=='Redmi' or data=='Samsung':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data =='below':
        mobiles=Product.objects.filter(category='M').filter (discounted_price__lt=155000)
    elif data =='above':
        mobiles=Product.objects.filter(category='M').filter (discounted_price__gt=155000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})


@login_required
def laptop(request,data=None):
    totalitem=0
    if request.user.is_authenticated:
              totalitem=len(Cart.objects.filter(user=request.user))
    if data == None:
        laptops=Product.objects.filter(category='L')
    elif data=='Hp' or data=='Asus':
        laptops=Product.objects.filter(category='L').filter(brand=data)
    elif data =='below':
        laptops=Product.objects.filter(category='L').filter (discounted_price__lt=65000)
    elif data =='above':
        laptops=Product.objects.filter(category='L').filter (discounted_price__gt=65000)
    return render(request, 'app/laptop.html',{'laptops':laptops,'totalitem':totalitem})

#def login(request):
 #return render(request, 'app/login.html')

#def customerregistration(request):
 #return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
    def get(self,request):
        totalitem=0
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Successfully Registered')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
    totalitem=0
    if request.user.is_authenticated:
              totalitem=len(Cart.objects.filter(user=request.user))
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=50.0
    totalamount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user== request.user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount
        totalamount=amount+shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items,'totalitem':totalitem})

@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")    



@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        totalitem=0
        if request.user.is_authenticated:
              totalitem=len(Cart.objects.filter(user=request.user))
        form =CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-success','totalitem':totalitem})
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        totalitem=0
        if request.user.is_authenticated:
              totalitem=len(Cart.objects.filter(user=request.user))
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Profile Updated Successfully')
        return render(request,'app/profile.html',
        {'form':form,'active':'btn-success','totalitem':totalitem})







@login_required
def search_venues(request):
    if request.method == "POST":
        searched=request.POST['searched']
        venues=Product.objects.filter(title__contains=searched)
        return render(request, 'app/search_venues.html',{'searched':searched,'venues':venues})
    else:        
        return render(request, 'app/search_venues.html')
