import json
import random
import os
from typing import List, Any

from IPython.core import page
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
# noinspection PyUnresolvedReferences
from mainapp.models import Product, ProductCategory

from basketapp.models import Basket

from basketapp.views import basket

from django.core.cache import cache

# def get_basket(user):
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     return []

def get_hot_product():
    products_list = Product.objects.all()
    return random.sample(list(products_list), 1)[0]

def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk).select_related('category')[:3]
    return same_products


def main(request):
    title = 'главная'
    products = Product.objects.all()[:4]

    content = {
        'title': title,
        'products': products,
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    title = 'продукты'
#    links_menu = ProductCategory.objects.all()
    links_menu = get_links_menu()
    page = request.GET.get('p', 1)

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все', 'pk': 0}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        paginator = Paginator(products, 2)

        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)


        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
        }
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'hot_product': hot_product,
    }
    return render(request, 'mainapp/products.html', content)

def product(request, pk):
    content = {
        'title': 'продукт',
        'product': get_object_or_404(Product, pk=pk),
        'links_menu': ProductCategory.objects.all(),
    }
    return render(request, 'mainapp/product.html', content)

def contact(request):
    title = 'о нас'
    locations = [
        {
            'city': 'Москва',
            'phone': '+7-888-888-8888',
            'email': 'info@stuls.ru',
            'address': 'Ул. Пушкина, д. Колотушкина'
        },
        {
            'city': 'Екатеринбург',
            'phone': '+7-777-777-7777',
            'email': 'info_yekaterinburg@stuls.ru',
            'address': 'Химмаш'
        },
        {
            'city': 'Владивосток',
            'phone': '+7-999-999-9999',
            'email': 'info_vladivistok@stuls.ru',
            'address': 'Прямо в порту'
        },
    ]

    content = {
        'title': title,
        'locations': locations,
    }
    return render(request, 'mainapp/contact.html', content)

def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)

def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)

def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')

def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)

def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')

def get_products_categiry_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
















