from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView

from .models import Product
from .serializers import ProductSerializer
from .forms import ProductImageForm


class ProductListAPI(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"


def gallery_view(request, *args, **kwargs):
    products = Product.objects.all().order_by("-date")
    context = {"products": products} 
    return render(request, "gallery/gallery.html", context)

    
def artwork_view(request, pk):
    product = get_object_or_404(Product.objects.select_related("artist").prefetch_related("carousel_images"),pk=pk)
    
    if request.method == "POST":
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.product = product         
            obj.save()
            return redirect("artworkDetail", pk=product.pk)  # go back to product page
    else:
        form = ProductImageForm()
        
    return render(request, "gallery/art_detail.html", {"form": form, "product": product})
    
    
#########################################################

def home_view(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    return render(request, "home.html", {})



def museum_view(request, *args, **kwargs):
    objs = Product.objects.all().order_by("date")
    context = {
        "products": objs
    }
    return render(request, "museum.html", context)
    
def map_view(request, *args, **kwargs):
    return render(request, "gallery/map.html", {})

def threeTest_view(request, *args, **kwargs):
    return render(request, "threeTest.html", {})



def contact_view(request, *args, **kwargs):
    return render(request, "contacts.html", {})