from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q
from django.db.models.functions import Lower

# Create your views here.


def filter_products_by_category(request, category_id):
    category_name = Category.objects.get(pk=category_id).name
    products = Product.objects.filter(category__pk=category_id)
    print('Products', products)
    return render(request, 'products/products.html', {'products': products, 'category_name': category_name})  # noqa:501


def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'products/products.html', {'products': products, 'query': query})  # noqa:501


def all_products(request):

    products = Product.objects.all()
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sort_k = request.GET['sort']
            sort = sort_k
            if sort_k == 'name':
                sort_k = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sort_k = f'-{sort_k}'
            products = products.order_by(sort_k)

    curr_sort = f'{sort}_{direction}'

    context = {
        'products': products,
        'curr_sort': curr_sort
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
