"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from shop import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('create/', views.createproduct, name='createproduct'),
    path('viewproduct<int:product_id>/', views.viewproduct, name='viewproduct'),
    path('dropproduct<int:product_id>/', views.dropproduct, name='dropproduct'),
    path('changeproduct<int:product_id>/', views.changeproduct, name='changeproduct'),
    path('addcart<int:product_id>/', views.addcart, name='addcart'),
    path('viewcart/', views.viewcart, name = 'viewcart'),
    path('clearcart/', views.clearcart, name = 'clearcart'),
    path('buycart/', views.buycart, name = 'buycart'),
    path('changecart<int:product_id><int:is_raise>', views.changecart, name = 'changecart'),

    path('signup/', views.signupuser, name = 'signup'),
    path('logout', views.logoutuser, name = 'logout'),
    path('login/', views.loginuser, name = 'login'),
]


urlpatterns += static(
    settings.MEDIA_URL,
    document_root = settings.MEDIA_ROOT
)



