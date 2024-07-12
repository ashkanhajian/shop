from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from card.cart import Cart


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'shop/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, slug=slug, id=id)
    cart = Cart(request)

    try:
        cart_quantity = cart.cart[str(id)]['quantity']
        count = product.inventory == cart_quantity
    except KeyError:
        count = False

    context = {
        'count': count,
        'cart': cart,
        'product': product,
    }
    return render(request, 'shop/detail.html', context)
