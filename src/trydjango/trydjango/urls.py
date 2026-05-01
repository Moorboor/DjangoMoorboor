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

from maps.views import ProductListAPI, map_view, museum_view, gallery_view, artwork_view, home_view, contact_view, threeTest_view, pdf_viewer_view, philosophy_view
from django.views.static import serve

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('home/', home_view, name='home'),
    path('contacts/', contact_view, name='contacts'),
    
    path('gallery/', gallery_view, name='gallery'),
    path('gallery/<int:pk>/', artwork_view, name='artworkDetail'), 
    path('api/artworks/', ProductListAPI.as_view()),
    path('home/threeTest/', threeTest_view, name='threeTest'),
    path('gallery/map/', map_view, name='map'),
    path('museum/', museum_view, name="museum"),
    path('philosophy/<str:filename>/', pdf_viewer_view, name='show_pdf'),
    path('philosophy', philosophy_view, name='philosophy'),
] 
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else: 
    urlpatterns += [
        path("media/<path:path>", serve, {"document_root": str(settings.MEDIA_ROOT)}),
    ]