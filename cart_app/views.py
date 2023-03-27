from django.shortcuts import render, redirect, get_object_or_404
from ecommerce_app.models import Product
from .models import Cart,CartItem,Order,OrderItem,ShippingAddress
from django.core.exceptions import ObjectDoesNotExist
from .forms import AddressForm
import razorpay
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    return redirect('cart_app:cart_detail')

def cart_detail(request,total=0,counter=0,cart_items=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,active=True)
        for cart_item in cart_items:
            global atotal
            total += (cart_item.product.price * cart_item.quantity)
            atotal = total*100

            counter += cart_item.quantity


    except ObjectDoesNotExist:
        pass

    return render(request,'cart.html',dict(cart_items=cart_items,total=total,atotal=atotal,counter=counter))

def cart_remove(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_app:cart_detail')

def full_remove(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product, id=product_id)
    cart_item=CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart_app:cart_detail')


def payment(request):
    cart_items = CartItem.objects.filter(cart=cart, active=True)
    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            amount = 50000

        client = razorpay.Client(
            auth=("rzp_test_ys4J6IcjWkJcuO", "k7YkmAxluuavZZMNFx9btugt"))

        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})
        return render(request, 'cart.html',{'payment':payment})
    return render(request, 'cart.html')

@csrf_exempt
def success(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart_app:cart_detail')


@csrf_exempt
def delete(request):
    cart = Cart.objects.all()
    cart_item = CartItem.objects.all()

    cart_item.delete()
    return redirect('cart_app:cart_detail')

