from django.shortcuts import render, get_object_or_404,redirect
from .models import Product,Category
from django.core.paginator import Paginator
from category.models import Category
from carts.views import _cart_id, is_product_in_cart
from django.db.models import Q

#===================== STORE PAGE =====================#
def store(request, category_slug=None):
    categories = Category.objects.all()
    products = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=selected_category, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
    
    # Check cart status for each product
    for product in products:
        product.in_cart = is_product_in_cart(request, product.id)
    
    product_count = products.count()
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    
    context = {
        'products': paged_product,
        'product_count': product_count,
        'categories': categories,
    }
    return render(request, 'store/store.html', context)

#===================== PRODUCT DETAIL PAGE =====================#
def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = is_product_in_cart(request, single_product.id)
        
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)




#================= SEARCH PRODUCT ========================================#
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)