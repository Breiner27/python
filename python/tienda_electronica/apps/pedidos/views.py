from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Pedido

@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_pedido')
    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos})

