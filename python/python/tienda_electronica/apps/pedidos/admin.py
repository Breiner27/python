from django.contrib import admin
from .models import Pedido, PedidoItem

class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'creado', 'estado')
    inlines = [PedidoItemInline]

admin.site.register(Pedido, PedidoAdmin)
admin.site.register(PedidoItem)


