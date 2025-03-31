from django.core.paginator import Paginator
from django.shortcuts import render
from products.models import Category, Product
from django.db.models import Q


def home(request):
    category_slug = request.GET.get('category')
    products = Product.objects.all()
    categories = Category.objects.all()

    if category_slug:
        products = products.filter(category__slug=category_slug)

    paginator = Paginator(products, 9)  # Har sahifada 9 ta mahsulot
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home/index.html', {'categories': categories, 'products': page_obj})


def search(request):
    query = request.GET.get('q', '')
    
    # Kategoriya bo'yicha qidiruv
    categories = Category.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    
    # Mahsulotlar bo'yicha qidiruv
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query) | Q(category__description__icontains=query)
    )
    
    return render(request, 'home/search_results.html', {
        'query': query,
        'categories': categories,
        'products': products
    })
