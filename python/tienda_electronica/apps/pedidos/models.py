from django.db import models
from apps.usuarios.models import UsuarioTienda  
from apps.productos.models import ProductosElectronicos

class Pedido(models.Model):
    usuario = models.ForeignKey(
        UsuarioTienda,
        related_name='pedidos', 
        on_delete=models.CASCADE
    )
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, default='Pendiente') 

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
