from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Имя')
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(db_index=True, verbose_name='активность', default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='имя')
    image = models.ImageField(upload_to='products_image', blank=True)
    short_desc = models.CharField(max_length=64, verbose_name='краткое описание', blank=True)
    description = models.TextField(blank=True, verbose_name='описание')
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveSmallIntegerField(verbose_name='количество на складе', default=0)
    is_active = models.BooleanField(db_index=True, verbose_name='активность', default=True)

    def __str__(self):
        return f'{self.name}({self.category.name})'





