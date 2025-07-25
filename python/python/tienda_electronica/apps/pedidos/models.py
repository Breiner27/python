from django.db import models
from apps.usuarios.models import UsuarioTienda  
from apps.productos.models import ProductosElectronicos

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Procesado', 'Procesado'),
        ('Enviado', 'Enviado'),
        ('Completado', 'Completado'),
        ('Cancelado', 'Cancelado'),
    ]

    METODO_PAGO_CHOICES = [
        ('TC', 'Tarjeta de crédito'),
        ('TD', 'Tarjeta de débito'),
        ('TB', 'Transferencia bancaria'),
        ('BV', 'Billetera virtual'),
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    
    # Nuevos campos
    metodo_pago = models.CharField(max_length=2, choices=METODO_PAGO_CHOICES, default='TC')
    banco = models.CharField(max_length=50, blank=True)

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username} - {self.estado}"


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(ProductosElectronicos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Pedido #{self.pedido.id})"
