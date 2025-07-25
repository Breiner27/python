from django.contrib import admin
from .models import CategoriaProducto, ProductosElectronicos, ImagenProducto, ResenaProducto


class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1
    fields = ['imagen', 'alt_text', 'es_principal', 'orden']


class ResenaProductoInline(admin.TabularInline):
    model = ResenaProducto
    extra = 0
    readonly_fields = ['fecha_resena']
    fields = ['usuario', 'calificacion', 'comentario', 'aprobada', 'fecha_resena']


@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa', 'fecha_creacion']
    list_filter = ['activa', 'fecha_creacion']
    search_fields = ['nombre']
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(ProductosElectronicos)
class ProductoElectronicoAdmin(admin.ModelAdmin):
    list_display = [
        'nombre', 'marca', 'modelo', 'precio', 'stock_cantidad',
        'stock_status', 'estado', 'destacado'
    ]
    list_filter = ['estado', 'destacado', 'categoria', 'marca']
    search_fields = ['nombre', 'marca', 'modelo', 'sku']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    autocomplete_fields = ['categoria']
    inlines = [ImagenProductoInline, ResenaProductoInline]
    
    def stock_status(self, obj):
        return "⚠️ Bajo" if obj.stock_cantidad < obj.stock_minimo else "✅ OK"
    stock_status.short_description = 'Stock'
    
    fieldsets = (
        ('📝 Información Básica', {
            'fields': ('nombre', 'descripcion', 'categoria', 'sku')
        }),
        ('📦 Detalles del Producto', {
            'fields': (
                'marca', 'modelo', 'precio', 'precio_oferta',
                'stock_cantidad', 'stock_minimo', 'estado', 'destacado',
                
            )
        }),
        ('🎨 Apariencia y Dimensiones', {
            'fields': ('color', 'peso', 'dimensiones'),
            'classes': ['collapse']  # Hace este grupo colapsable
        }),
        ('⚙️ Especificaciones Técnicas', {
            'fields': ('especificaciones_tecnicas',),
            'classes': ['collapse']  # También colapsable
        }),
        ('📅 Fechas de Registro', {
            'fields': ('fecha_creacion', 'fecha_actualizacion')
        }),
    )
# Register your models here.
