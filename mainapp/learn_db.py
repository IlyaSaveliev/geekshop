from django.core.management import BaseCommand
from django.db.models import Q, F, When, Case, DecimalField, IntegerField
from mainapp.models import Product
from datetime import timedelta
from ordersapp.models import OrderItem

class Command(BaseCommand):

    def handle(self, *args, **options):

        action_1 = 1
        action_2 = 2
        action_expired = 3

        action_1_timedelta = timedelta(hours=12)
        action_2_timedelta = timedelta(days=1)

        action_1_discount = 0.3
        action_2_discount = 0.15
        action_expired_discount = 0.05
 
        action_1_condition = Q(order__updated__lte=F('order__created') + action_1_time_delta)
        action_2_condition = Q(order__updated__lte=F('order__created') + action_2_time_delta) & \
                             Q(order__updated__gt=F('order__created') + action_1_time_delta)
        action_expired_condition = Q(order__updated__gt=F('order__created') + action_2_time_delta)

        action_1_order = When(action_1_condition, then=action_1)
        action_2_order = When(action_2_condition, then=action_2)
        action_expired_order = When(action_expired_condition, then=action_expired)

        action_1_price = When(action_1_condition, then=F('product__price') * F('quantity') * action_1_discount)
        action_2_price = When(action_2_condition, then=F('product__price') * F('quantity') * action_2_discount)
        action_expired_price = When(action_expired_condition, then=F('product__price') * F('quantity') * action_expired_discount)

        orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1_order,
                action_2_order,
                action_expired_order,
                output_field=IntegerField()
            )
        ).annotate(
            total_price=Case(
                action_1_price,
                action_2_price,
                action_expired_price,
                output_field=DecimalField()
            )
        ).order_by('action_order', 'total_price').select_related()

        for orderitem in test_orders:
            print(f'{orderitem.action_order:2}: заказ №{orderitem.pk:3}:\
                    {orderitem.product.name:15}: скидка\
                    {abc(orderitem.total_price):6.2f} руб. | \
                    {orderitem.order.upload - orderitem.order.created}')
