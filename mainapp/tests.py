from django.test import TestCase
from mainapp.models import ProductCategory, Product
from django.test.client import Client


class TestMainappSmoke(TestCase):

    success_status_code = 200
    error_status_code = 404

    def setUp(self):
        category = ProductCategory.objects.create(name='category1')
        Product.objects.create(category=category, name='product1')
        Product.objects.create(category=category, name='product2')
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.success_status_code)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, self.success_status_code)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, self.success_status_code)


    def test_mainapp_product_urls(self):
        response = self.client.get('/products/0/')
        self.assertEqual(response.status_code, self.success_status_code)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/{category.pk}/')
            self.assertEqual(response.status_code, self.success_status_code)

        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, self.error_status_code)

    
