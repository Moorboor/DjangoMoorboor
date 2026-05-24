from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView
from .models import Product, ProductVisit
from django.db.models import F

from .models import Product
from .serializers import ProductSerializer
from .forms import ProductMediaForm


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
    prev_product = Product.objects.filter(date__lt=product.date).order_by('-date').first()
    next_product = Product.objects.filter(date__gt=product.date).order_by('date').first()
    
    # if request.method == "POST":
    #     form = ProductMediaForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         obj = form.save(commit=False)
    #         obj.product = product         
    #         obj.save()
    #         return redirect("artworkDetail", pk=product.pk)  # go back to product page
    # else:
    #     form = ProductMediaForm()  
        
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    visit_created = ProductVisit.objects.get_or_create(
        product=product,
        session_key=session_key
    )[1]  # [1] gives us the boolean "created"
    
    # Update the denormalized visit count if this is a new visit
    if visit_created:
        Product.objects.filter(pk=product.pk).update(visit_count=F('visit_count') + 1)
        product.refresh_from_db()
    
    context = {
        'product':      product,
        'prev_product': prev_product,
        'next_product': next_product,
        # "form": form
    }
    return render(request, "gallery/art_detail.html", context=context)

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

def university_view(request, *args, **kwargs):
    return render(request, "university.html", {})


def pdf_viewer_view(request, filename, *args, **kwargs):
    pdf_path = f'university/{filename}'
    
    context = {
        'pdf_path': pdf_path,
        'pdf_name': filename.replace('_', ' ').replace('.pdf', '').title()
    }
    return render(request, 'pdfViewer.html', context)



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Get or create session key
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    # Register the visit (only once per session)
    visit_created = ProductVisit.objects.get_or_create(
        product=product,
        session_key=session_key
    )[1]  # [1] gives us the boolean "created"
    
    # Update the denormalized visit count if this is a new visit
    if visit_created:
        Product.objects.filter(pk=product.pk).update(visit_count=F('visit_count') + 1)
        # Refresh the product instance to get the updated count
        product.refresh_from_db()
    
    context = {
        'product': product,
    }
    return render(request, 'product_detail.html', context)