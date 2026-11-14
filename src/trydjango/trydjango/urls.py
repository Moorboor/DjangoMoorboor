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

from maps import views
from django.views.static import serve

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home_view, name='home'),
    path('admin/', admin.site.urls),
    path('home/', views.home_view, name='home'),
    path('contacts/', views.contact_view, name='contacts'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('gallery/<int:pk>/', views.artwork_view, name='artworkDetail'), 
    path('api/artworks/', views.ProductListAPI.as_view()),
    path('home/threeTest/', views.threeTest_view, name='threeTest'),
    path('gallery/map/', views.map_view, name='map'),
    path('museum/', views.museum_view, name="museum"),
    path('university/<str:filename>/', views.pdf_viewer_view, name='show_pdf'),
    path('university', views.university_view, name='university'),
    path('artwork/<int:pk>/comment/', views.add_comment, name='add_comment'),
] 
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else: 
    urlpatterns += [
        path("media/<path:path>", serve, {"document_root": str(settings.MEDIA_ROOT)}),
    ]