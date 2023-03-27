from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product,Wishlist
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.http import JsonResponse
import json
from django.views.decorators.http import  require_GET
from ecommerce_app.form import CustomUserForm
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
#
# def index(request):
#     return HttpResponse("hey am here")

def allProdCat(request, c_slug=None):
    c_page = None
    products = None
    if c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        products = Product.objects.all().filter(category=c_page, available=True)
    else:

        products = Product.objects.all().filter(available=True)
    paginator = Paginator(products, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except(EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, "category.html", {'category': c_page, 'products': products})


def proDetail(request, c_slug, product_slug):
    if request.user.is_authenticated:
        try:
            product = Product.objects.get(category__slug=c_slug, slug=product_slug)
            wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        except Exception as e:
            raise e
        return render(request, 'product.html', {'product': product})
    else:
        return redirect("/register")


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request, "Logged out Successfully")
    return redirect("/")


def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect("/")
            else:
                messages.error(request, "Invalid User Name or Password")
                return redirect("/login")
        return render(request, 'login.html')


def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Success You can Login Now..!")
            return redirect('/login')
    return render(request, 'register.html', {'form': form})


# favorite view code
def favviewpage(request):
    if request.user.is_authenticated:
        fav = Wishlist.objects.filter(user=request.user)
        return render(request, "fav.html", {"fav": fav})
    else:
        return redirect("/")


def remove_fav(request, product_id):
    item = Wishlist.objects.get(id=product_id)
    item.delete()
    return redirect("/favviewpage")


def add_favorite(request, product_id):
    try:
        Wishlist.objects.get(user=request.user, product_id=(product_id))
        messages.warning(request,"this product is already in your favorites")
        return redirect(request.META.get('HTTP_REFERER'))
    except ObjectDoesNotExist:
        Wishlist.objects.create(user=request.user, product_id=(product_id))
        messages.success(request, "product add favorite")
        return redirect(request.META.get('HTTP_REFERER'))
