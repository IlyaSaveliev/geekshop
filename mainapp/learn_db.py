from django.core.management import BaseCommand
from django.db.models import Q
from mainapp.models import Product

class Command(BaseCommand):

    def handle(self, *args, **options):

        home_query = (category__name='дом')
        office_query = (category__name='офис')
        
        products = Product.objects.filter(
            home_query | office_query
        )