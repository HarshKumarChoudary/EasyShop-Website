from django.shortcuts import render,redirect
from django.views import View
from .forms import CustomerRegistration,loginform,customerprofileform,buyeraddress
from .models import cart,buyer,seller,address,gender,category,product,order_placed
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def home(request):
    return redirect('/buyers')

def seller(request):
    return render(request,'app/seller.html')


class buyers(View):
    def get(self,request):
        totalitem=0
        fashion = product.objects.filter(category=category.objects.get(name = 'Fashion').id)
        electronics = product.objects.filter(category=category.objects.get(name = 'Electronics').id)
        stationary = product.objects.filter(category=category.objects.get(name = 'Stationary').id)
        topwear = product.objects.filter(category=category.objects.get(name = 'TopWears').id)
        frontwear = product.objects.filter(category=category.objects.get(name = 'FrontWears').id)
        #services = product.objects.filter(category=category.objects.get(name = 'Services').id)
        dailyneeds = product.objects.filter(category = category.objects.get(name = 'DailyNeeds').id) 
        if request.user.is_authenticated:
            if buyer.objects.filter(user=request.user).exists():
                totalitem = len(cart.objects.filter(buyer=buyer.objects.get(user=request.user)))
        return render(request,'app/buyer.html',{'fashion':fashion,'electronics':electronics,'stationary':stationary,'topwear':topwear,'frontwear':frontwear,'dailyneeds':dailyneeds,'total':totalitem})


class product_detail(View):
    def get(self,request,pk):
        totalitem=0
        if request.user.is_authenticated:
           totalitem = len(cart.objects.filter(buyer=buyer.objects.get(user=request.user)))
        
        Product = product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated :
            item_already_in_cart=cart.objects.filter(Q(product=Product.id)&Q(buyer=buyer.objects.get(user=request.user)))
        return render(request,'app/productdetail.html',{'product':Product,'item_already':item_already_in_cart,'total':totalitem})

@login_required
def add_to_cart(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(cart.objects.filter(buyer=buyer.objects.get(user=request.user)))
    buy= buyer.objects.get(user=request.user)
    Product_id=request.GET.get('prod_id')
    cart(buyer=buy,product=product.objects.get(id=Product_id)).save()
    return redirect('/cart',{'total':totalitem})

@login_required
def show_cart(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(cart.objects.filter(buyer=buyer.objects.get(user=request.user)))
    if request.user.is_authenticated:
        buy_person= buyer.objects.get(user=request.user)
        carts=cart.objects.filter(buyer=buy_person)
        shippint_amt = 70.0
        total_amount=0.0
        amount = 0
        cart_product=[p for p in cart.objects.all() if p.buyer==buy_person]
        if cart_product:
            for p in cart_product:
                temp_amt = (p.quantity*p.product.discount_price)
                amount+=temp_amt
            total_amount=amount+shippint_amt
            return render(request, 'app/addtocart.html',{'carts':carts,'total_amount':total_amount,'amount':amount,'total':totalitem})
        else:
            return render(request,'app/emptycart.html',{'total':totalitem})


def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=cart.objects.get(Q(product=prod_id)& Q(buyer=buyer.objects.get(user=request.user)))
        c.quantity+=1
        c.save()
        shippint_amt = 70.0
        total_amount=0.0
        amount = 0
        buy_person= buyer.objects.get(user=request.user)
        cart_product=[p for p in cart.objects.all() if p.buyer==buy_person]
        for p in cart_product:
            temp_amt = (p.quantity*p.product.discount_price)
            amount+=temp_amt
        total_amount=amount+shippint_amt
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'total_amount':total_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=cart.objects.get(Q(product=prod_id)& Q(buyer=buyer.objects.get(user=request.user)))
        c.quantity-=1
        c.save()
        shippint_amt = 70.0
        total_amount=0.0
        amount = 0
        buy_person= buyer.objects.get(user=request.user)
        cart_product=[p for p in cart.objects.all() if p.buyer==buy_person]
        for p in cart_product:
            temp_amt = (p.quantity*p.product.discount_price)
            amount+=temp_amt
        total_amount=amount+shippint_amt
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'total_amount':total_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=cart.objects.get(Q(product=prod_id)& Q(buyer=buyer.objects.get(user=request.user)))
        c.delete()
        shippint_amt = 70.0
        total_amount=0.0
        amount = 0
        buy_person= buyer.objects.get(user=request.user)
        cart_product=[p for p in cart.objects.all() if p.buyer==buy_person]
        for p in cart_product:
            temp_amt = (p.quantity*p.product.discount_price)
            amount+=temp_amt
        total_amount=amount+shippint_amt
        data = {
            'amount':amount,
            'total_amount':total_amount
        }
        return JsonResponse(data)



def buy_now(request):
 return render(request, 'app/buynow.html')


@method_decorator(login_required,name='dispatch')
class profileview(View):
    def get(self,request):
        totalitem=0
        if request.user.is_authenticated:
            if buyer.objects.filter(user=request.user).exists():
                totalitem = len(cart.objects.filter(buyer=buyer.objects.get(user=request.user)))
        form=customerprofileform()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','total':totalitem})

    def post(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(cart.objects.filter(buyer=buyer.objects.get(user=request.user)))
        form =customerprofileform(request.POST, request.FILES)
        if form.is_valid():
            if buyer.objects.filter(user=request.user).exists():
                buy=buyer.objects.get(user=request.user)
                buy.name=form.cleaned_data['name']
                buy.gen=form.cleaned_data['gen']
                buy.email=form.cleaned_data['email']
                buy.phone_number=form.cleaned_data['phone_number']
                buy.save()
            else:
                old=form.save(commit=False)
                old.user=request.user
                old.save()
            messages.success(request,'Congratulation! Profile Updated Successfully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','total':totalitem})
            

class addres(View):
    
    def get(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(cart.objects.filter(buyer=buyer.objects.get(user=request.user)))
        form = buyeraddress()
        add = address.objects.filter(user=request.user)
        return render(request, 'app/address.html',{'add':add,'form':form,'active':'btn-primary','total':totalitem})

    def post(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(cart.objects.filter(buyer=buyer.objects.get(user=request.user)))
        form=buyeraddress(request.POST,request.FILES)
        if form.is_valid:
            old=form.save(commit=False)
            old.user=request.user
            old.save()
        add = address.objects.filter(user=request.user)
        form2=buyeraddress()
        return render(request, 'app/address.html',{'add':add,'form':form2,'active':'btn-primary','total':totalitem})

@login_required
def orders(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(cart.objects.filter(buyer=buyer.objects.get(user=request.user)))
    op = order_placed.objects.filter(buyer=buyer.objects.get(user=request.user))
    return render(request, 'app/orders.html',{'orders':op,'total':totalitem})

def mobile(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(cart.objects.filter(buyer=buyer.objects.get(user=request.user)))
    mobiles = product.objects.filter(category=category.objects.get(name = 'Mobiles').id)
    return render(request, 'app/mobile.html',{'mobiles':mobiles,'total':totalitem})


class CustomerRegistrationView(View):
    
    def get(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(cart.objects.filter(buyer=buyer.objects.get(user=request.user)))
        form = CustomerRegistration()
        return render(request,'app/customerregistration.html',{'form':form,'total':totalitem})
    
    def post(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(cart.objects.filter(buyer=buyer.objects.get(user=request.user)))
        form = CustomerRegistration(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations! Registered Successfully')
            form.save()
        
        return render(request,'app/customerregistration.html',{'form':form,'total':totalitem})

@login_required
def checkout(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(cart.objects.filter(buyer=buyer.objects.get(user=request.user)))
    user=request.user
    add= address.objects.filter(user=user)
    cart_items=cart.objects.filter(buyer=buyer.objects.get(user=request.user))
    amount=0.0
    shipping=70
    total_amt=0
    buy_person=buyer.objects.get(user=request.user)
    cart_product=[p for p in cart.objects.all() if p.buyer == buyer.objects.get(user=request.user)]
    if cart_product :
        for p in cart_product :
            temp_amt=(p.quantity*p.product.discount_price)
            amount+=temp_amt
        total_amt+=amount+shipping
    return render(request, 'app/checkout.html',{'add':add,'total_amt':total_amt,'buyer':buy_person,'cart_items':cart_items,'total':totalitem})

@login_required
def payment_done(request):
    
    delivaryadd=request.GET.get('custid')
    deliveryadd = address.objects.get(pk=delivaryadd)
    user=request.user
    buyerobj=buyer.objects.get(user=user)
    carts = cart.objects.filter(buyer=buyerobj)
    for c in carts :
        order_placed(deliveryaddress=deliveryadd,buyer=buyerobj,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("/orders")
