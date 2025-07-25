from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Carrito, CarritoItem
from apps.productos.models import ProductosElectronicos
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import messages
from apps.pedidos.models import Pedido, PedidoItem
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.db import transaction
from django.views.decorators.http import require_GET
from django.template.loader import render_to_string




@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(ProductosElectronicos, id=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))

    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    item, creado_item = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

    if not creado_item:
        item.cantidad += cantidad
    else:
        item.cantidad = cantidad

    item.save()
    return redirect('carrito:ver_carrito')  # Ajusta la URL a tu vista para ver carrito


@require_POST
@login_required
def agregar_al_carrito_ajax(request):
    producto_id = request.POST.get('producto_id')
    producto = get_object_or_404(ProductosElectronicos, id=producto_id)

    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    item, creado = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

    if creado:
        item.cantidad = 1
        item.save()
        en_carrito = True
    else:
        item.delete()
        en_carrito = False
    total_items = carrito.items.aggregate(total=Sum('cantidad'))['total'] or 0

    return JsonResponse({
        'success': True,
        'mensaje': f'Producto {"agregado" if en_carrito else "eliminado"} del carrito.',
        'total_items': total_items,
        'en_carrito': en_carrito
    })

@login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()

    contexto = {
        'carrito': carrito,
        'items': items,
    }
    return render(request, 'carrito/ver_carrito.html', contexto)

@login_required
def eliminar_item_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, carrito__usuario=request.user)
    item.delete()
    return redirect('carrito:ver_carrito')

@login_required
@transaction.atomic
def realizar_compra(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)

    if not carrito.items.exists():
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('carrito:ver_carrito')

    # ✅ Recuperar método de pago y banco desde el formulario
    metodo_pago = request.POST.get('metodo_pago', 'TC')  # Default: tarjeta crédito
    banco = request.POST.get('banco', '').strip()

    # ✅ Solo guardar banco si el método de pago es transferencia bancaria
    if metodo_pago != 'TB':
        banco = ''

    # Crear el pedido
    pedido = Pedido.objects.create(
        usuario=request.user,
        total=0,  # se actualiza luego
        estado='Pendiente',
        metodo_pago=metodo_pago,
        banco=banco
    )

    total = 0
    for item in carrito.items.select_related('producto'):
        producto = item.producto
        if not producto.reducir_stock(item.cantidad):
            messages.error(request, f"Stock insuficiente para {producto.nombre}.")
            pedido.delete()
            return redirect('carrito:ver_carrito')

        PedidoItem.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=item.cantidad
        )
        total += producto.precio * item.cantidad

    pedido.total = total
    pedido.save()

    carrito.items.all().delete()

    messages.success(request, "Compra realizada con éxito.")
    return redirect('productos:lista')

@login_required
@require_GET
def obtener_estado_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    productos = carrito.items.values_list('producto_id', flat=True)
    total = carrito.items.aggregate(total=Sum('cantidad'))['total'] or 0

    return JsonResponse({
        'success': True,
        'productos_en_carrito': list(productos),
        'total_items': total
    })
    
@login_required
@require_GET
def cargar_modal_pago(request):
     return render(request, 'carrito/modal_pago.html')
