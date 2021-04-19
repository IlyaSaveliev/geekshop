from django.contrib import admin
# noinspection PyUnresolvedReferences
from mainapp.models import ProductCategory, Product



admin.site.register(ProductCategory)
admin.site.register(Product)
