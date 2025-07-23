from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect 

urlpatterns = [
    path('', lambda request: redirect('productos:inicio')), 
    path('admin/', admin.site.urls),
    path('usuarios/', include('apps.usuarios.urls')),
    path('productos/', include('apps.productos.urls')), 
    path('carrito/',include('apps.carrito.urls')),
    path('pedidos/', include('apps.pedidos.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
