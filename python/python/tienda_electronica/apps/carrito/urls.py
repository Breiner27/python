from django.urls import path
from . import views

app_name = 'carrito'

urlpatterns = [
    path('', views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar'),
    path('agregar/ajax/', views.agregar_al_carrito_ajax, name='agregar_ajax'),
    path('eliminar/<int:item_id>/', views.eliminar_item_carrito, name='eliminar_item_carrito'),
    path('realizar-compra/', views.realizar_compra, name='realizar_compra'),
    path('estado/', views.obtener_estado_carrito, name='obtener_estado'),
    path('modal-pago/', views.cargar_modal_pago, name='cargar_modal_pago'),
]
