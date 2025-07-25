from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('',views.inicio,name='inicio'),
    path('lista', views.ListaProductosView.as_view(), name='lista'),
    path('producto/<int:pk>/', views.DetalleProductoView.as_view(), name='detalle'),
    path('crear/', views.CrearProductoView.as_view(), name='crear'),
    path('editar/<int:pk>/', views.EditarProductoView.as_view(), name='editar'),
    path('eliminar/<int:pk>/', views.EliminarProductoView.as_view(), name='eliminar'),
    path('categoria/<slug:slug>/', views.productos_por_categoria, name='por_categoria'),
    path('resena/<int:producto_id>/', views.agregar_resena, name='agregar_resena'),
    path('categoria/<slug:slug>/', views.productos_por_categoria, name='por_categoria'),
    path('favorito/ajax/', views.toggle_favorito_ajax, name='toggle_favorito_ajax'),
    path('favoritos/', views.lista_favoritos, name='favoritos'),
]