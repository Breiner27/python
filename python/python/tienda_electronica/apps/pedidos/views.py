from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.pedidos.models import Pedido, PedidoItem
from apps.carrito.models import Carrito
from django.contrib import messages
from .models import Pedido

@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_pedido')
    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos})

@login_required
@transaction.atomic
def realizar_compra(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()
    
    if not carrito or not carrito.items.exists():
        messages.error(request, "Tu carrito está vacío.")
        return redirect('carrito:ver')  # Ajusta si el nombre es diferente

    pedido = Pedido.objects.create(usuario=request.user)

    for item in carrito.items.all():
        producto = item.producto
        if producto.reducir_stock(item.cantidad):  # Usa tu método aquí
            PedidoItem.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=item.cantidad
            )
        else:
            messages.error(request, f"Stock insuficiente para {producto.nombre}.")
            pedido.delete()  # Cancela el pedido
            return redirect('carrito:ver')

    # Calcular total del pedido
    pedido.total = sum(item.producto.precio * item.cantidad for item in carrito.items.all())
    pedido.save()

    # Vaciar carrito
    carrito.items.all().delete()

    messages.success(request, "¡Compra realizada con éxito!")
    return redirect('perfil:mis_pedidos')