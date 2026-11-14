from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView
from .models import Product, ProductVisit
from django.db.models import F
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Product, Comment


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

    
def gallery_view(request):
    """Gallery with pagination, region and category filters"""
    # Get filter parameters from URL (both can be empty)
    region = request.GET.get('region', '')
    category = request.GET.get('category', '')
    
    # Base queryset
    products = Product.objects.all().order_by('-date')
    
    # Filter by region if specified
    if region and region != '':
        products = products.filter(region=region)
    
    # Filter by category if specified (works independently of region)
    if category and category != '':
        products = products.filter(category=category)
    
    # Pagination
    paginator = Paginator(products, 16)  # 24 items per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get all available regions
    all_regions = ['Svalbard', 'Central America', 'Uzbekistan', 'Europe']
    
    # Get all unique categories (from entire database)
    all_categories = Product.objects.values_list('category', flat=True).distinct().order_by('category')
    
    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'region': region,
        'category': category,
        'regions': all_regions,
        'all_categories': all_categories,
    }
    
    return render(request, 'gallery/gallery.html', context)
    



def artwork_view(request, pk):
    """Display artwork detail with comments"""
    product = get_object_or_404(Product, pk=pk)
    
    # Increment visit count
    product.visit_count += 1
    product.save(update_fields=['visit_count'])
    
    try:
        prev_product = Product.objects.filter(date__lt=product.date).order_by('-date').first()
        next_product = Product.objects.filter(date__gt=product.date).order_by('date').first()
    except ValueError:
        prev_product = None
        next_product = None
    
    # Get comments
    comments = product.comments.filter(is_approved=True)
    
    context = {
        'product': product,
        'prev_product': prev_product,
        'next_product': next_product,
        'comments': comments,
    }
    return render(request, 'gallery/art_detail.html', context)


@require_http_methods(['POST'])
def add_comment(request, pk):
    """Add a comment to an artwork"""
    product = get_object_or_404(Product, pk=pk)
    
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    content = request.POST.get('content', '').strip()
    
    if name and email and content:
        Comment.objects.create(
            product=product,
            name=name,
            email=email,
            content=content,
        )
        messages.success(request, 'Comment posted successfully!')
    else:
        messages.error(request, 'Please fill in all fields.')
    
    return redirect('artworkDetail', pk=pk)


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


def home_view(request, *args, **kwargs):
    """Home page with region previews"""
    print(args, kwargs)
    print(request.user)
    regions = {
        'Svalbard': Product.objects.filter(region='Svalbard').order_by('-visit_count')[:8],
        'Central America': Product.objects.filter(region='Central America').order_by('-date')[:8],
        'Uzbekistan': Product.objects.filter(region='Uzbekistan').order_by('-date')[:8],
        'Europe': Product.objects.filter(region='Europe').order_by('-date')[:8],
    }
    
    # Get counts for each region
    counts = {
        'Svalbard': Product.objects.filter(region='Svalbard').count(),
        'Central America': Product.objects.filter(region='Central America').count(),
        'Uzbekistan': Product.objects.filter(region='Uzbekistan').count(),
        'Europe': Product.objects.filter(region='Europe').count(),
    }
    
    # Build category_data structure
    category_data = {}
    for region_name in regions:
        category_data[region_name] = {
            'count': counts[region_name],
            'products': regions[region_name],  # List of Product objects
        }
    
    context = {
        'categories': ['Svalbard', 'Central America', 'Uzbekistan', 'Europe'],  # Just the names
        'category_data': category_data,  # Dictionary with count + products
    }
    return render(request, 'home.html', context)
