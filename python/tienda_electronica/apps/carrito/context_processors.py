from .models import Carrito
from django.db.models import Sum

def carrito_context(request):
    if request.user.is_authenticated:
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        total = carrito.items.aggregate(total=Sum('cantidad'))['total'] or 0
    else:
        total = 0
    return {'total_items_carrito': total}
