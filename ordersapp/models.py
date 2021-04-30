from django.conf import settings
from django.db import models

from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATYSES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PROCEEDED, 'обработан'),
        (PAID, 'оплачен'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменён'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name='заказ создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='заказ был изменён')
    status = models.CharField(choices=ORDER_STATYSES, default=FORMING, max_length=3, verbose_name='статус')
    is_active = models.BooleanField(default=True, verbose_name='активен')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Текущий заказ: {self.pk}'

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_total_cost(self):
        items = self.orderitems.select_related()
        # return sum(list(map(lambda x: x.get_product_cost, items)))
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }


    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    def get_product_cost(self):
        return self.quantity * self.product.price

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)