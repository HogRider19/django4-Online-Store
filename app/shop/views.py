from itertools import product
from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Product, Category
from .forms import ProductForm
from cart.cart import Cart

def home(request):
    page = int(request.GET.get('page', 1))

    previousPage = page - 1 if page != 1 else 1
    nextPage = page + 1

    products = Product.objects.all()[(page-1)*9:(page-1)*9+9]

    return render(request, 'shop/home.html',{'products':products, 'pageinfo':{'next': nextPage, 'previous': previousPage}})


@login_required
def userorders(request, user_id):
    pass


def viewcart(request):
    cart = Cart(request)
    return render(request, 'shop/viewcart.html', {'cart':cart, 'info':{'count':len(cart)}})


def addcart(request, product_id):
    product = Product.objects.get(pk = product_id)
    cart = Cart(request)
    cart.add(product)
    cart.save()
    return redirect('home')


def viewproduct(request, product_id):
    product = Product.objects.get(pk = product_id)
    product_user_id = product.user.id
    is_change = True if request.user.id == product_user_id else False
    return render(request, 'shop/viewproduct.html', {'product': product, 'is_change':is_change})


def changeproduct(request, product_id):
    product = get_object_or_404(Product, pk = product_id, user = request.user)
    if request.method == 'GET':
        category = Category.objects.all()
        info = {
            'name':product.name,
            'description':product.description,
            'count_sell':product.count_sell,
            'image':product.image,
            'price':int(product.price),
            'category':product.category
        }
        return render(request, 'shop/changeproduct.html', {'info':info, 'category':category})
    else:
        try:
            rg = request.POST
            product.name = rg['name']
            product.description = rg['description']
            if rg['image'] != '':
                print(rg['image'])
                product.image = rg['image']
            product.price = rg['price']
            product.count_sell = rg['count_sell']
            product.category = Category.objects.get(pk = rg['category'])
            product.user = request.user
            product.save()
            return redirect('home')
        except ValueError:
            return render(request, 'shop/changeproduct.html', {'form':ProductForm(), 'error':'Некорректные данные'})

def dropproduct(request, product_id):
    product = get_object_or_404(Product, pk = product_id, user = request.user)
    product.delete()
    return redirect('home')


@login_required
def createproduct(request):
    if request.method == 'GET':
        category = Category.objects.all()
        return render(request, 'shop/createproduct.html', {'form':ProductForm(), 'category':category})
    else:
        try:
            rg = request.POST
            newProduct = Product()
            newProduct.name = rg['name']
            newProduct.description = rg['description']
            newProduct.image = rg['image']
            newProduct.price = rg['price']
            newProduct.count_sell = rg['count_sell']
            newProduct.category = Category.objects.get(pk = rg['category'])
            newProduct.user = request.user
            newProduct.save()
            return redirect('home')
        except ValueError:
            return render(request, 'shop/createproduct.html', {'form':ProductForm(), 'error':'Некорректные данные'})


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'shop/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'shop/signup.html', {'form': UserCreationForm(), 'error': 'Имя пользователя уже занято'})
        else:
            return render(request, 'shop/signup.html', {'form': UserCreationForm(), 'error': 'Пароли не совпадают'})

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'shop/login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            return render(request, 'shop/login.html', {'form':AuthenticationForm(), 'error':'Неправельный логин или пароль'})
        else:
            login(request, user)
            return redirect('home')
