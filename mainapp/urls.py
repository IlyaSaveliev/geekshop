from django.urls import path
# noinspection PyUnresolvedReferences
from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='products'),
    path('<int:pk>/', mainapp.products, name='category'),
    # path('<int:pk>/<int:page>/', mainapp.products, name='page'),
    path('product/<int:pk>', mainapp.product, name='product'),
]
