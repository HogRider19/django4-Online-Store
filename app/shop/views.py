from itertools import product
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Product, Category
from .forms import ProductForm

def home(request):
    page = int(request.GET.get('page', 1))

    previousPage = page - 1 if page != 1 else 1
    nextPage = page + 1

    products = Product.objects.all()[(page-1)*9:(page-1)*9+9]

    return render(request, 'shop/home.html',{'products':products, 'pageinfo':{'next': nextPage, 'previous': previousPage}})


@login_required
def userorders(request, user_id):
    pass


@login_required
def createproduct(request):
    if request.method == 'GET':
        category = Category.objects.all()
        return render(request, 'shop/createproduct.html', {'form':ProductForm(), 'category':category})
    else:
        #try:
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
        #except ValueError:
        #    return render(request, 'shop/createproduct.html', {'form':ProductForm(), 'error':'Некорректные данные'})


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
