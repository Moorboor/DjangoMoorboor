"""
URL configuration for trydjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from maps.views import map_detail_view, ProductListAPI, museum_view, product_view, home_view, SvalbardArt_view, contact_view, threeTest_view


from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home_view, name='home'),
    path('home/', home_view, name='home'),
    path('contacts/', contact_view, name='contacts'),
    path('SvalbardArt/', SvalbardArt_view, name='SvalbardArt'),
    path('admin/', admin.site.urls),
    path('maps/', map_detail_view, name='map-detail'),
    path('maps/<int:pk>/', product_view, name='artDetail'), 
    path('home/threeTest/', threeTest_view, name='threeTest'),
    path('api/products/', ProductListAPI.as_view()),
    path('museum/', museum_view, name="museum"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
