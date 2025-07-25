from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('mis-pedidos/', views.lista_pedidos, name='mis_pedidos'),
    path('realizar/', views.realizar_compra, name='realizar_compra'),
]
