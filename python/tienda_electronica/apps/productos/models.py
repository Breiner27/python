from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator,MaxValueValidator
from django.urls import reverse
from decimal import Decimal
from apps.usuarios.models import UsuarioTienda

class CategoriaProducto(models.Model):
    nombre=models.CharField(max_length=100,unique=True)
    descripcion=models.TextField(blank=True)
    slug=models.SlugField(max_length=100,unique=True,blank=True)
    activa=models.BooleanField(default=True)
    fecha_creacion=models.DateTimeField(auto_now_add=True)
    imagen=models.ImageField(upload_to='categorias/',blank=True)

    class Meta:
        db_table='categoria_productos'
        verbose_name='Categoria'
        verbose_name_plural='Categorias'
        ordering=['nombre']

    def save(self, *args, **kwargs):
        if not self.slug:
             self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('productos: por_categoria',kwargs={'slug':self.slug})

    def __str__(self):
        return self.nombre

class ProductosElectronicos(models.Model):
    ESTADO_PRODUCTOS=[
        ('disponible','Disponible'),
        ('agotado','agotado'),
        ('descontinuado','Descontinuado'),
        ('preventa','pre-venta'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    precio_oferta = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    stock_cantidad = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=1)
    sku = models.CharField(max_length=50, unique=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    especificaciones_tecnicas = models.JSONField(default=dict, blank=True)
    color = models.CharField(max_length=50, blank=True)
    peso = models.DecimalField(
        max_digits=8, 
        decimal_places=3, 
        null=True, 
        blank=True,
        help_text="Peso en kilogramos"
    )
    dimensiones = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Formato: Alto x Ancho x Profundidad en cm"
    )
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_PRODUCTOS, 
        default='disponible'
    )
    destacado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey(
        CategoriaProducto, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='productos'
    )
    usuario_creador = models.ForeignKey(
        UsuarioTienda, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='productos_creados'
    )
    
    class Meta:
        db_table = 'producto_electronico'
        verbose_name = 'Producto Electrónico'
        verbose_name_plural = 'Productos Electrónicos'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['marca', 'modelo']),
            models.Index(fields=['estado']),
            models.Index(fields=['destacado']),
        ]
    
    @property
    def disponible(self):
        return self.estado == 'disponible' and self.stock_cantidad > 0
    
    @property
    def precio_actual(self):
        return self.precio_oferta if self.precio_oferta else self.precio
    
    @property
    def tiene_oferta(self):
        return self.precio_oferta is not None and self.precio_oferta < self.precio
    
    @property
    def descuento_porcentaje(self):
        if self.tiene_oferta:
            return round(((self.precio - self.precio_oferta) / self.precio) * 100)
        return 0
    
    @property
    def stock_bajo(self):
        return self.stock_cantidad <= self.stock_minimo
    
    def reducir_stock(self, cantidad):
        if self.stock_cantidad >= cantidad:
            self.stock_cantidad -= cantidad
            if self.stock_cantidad == 0:
                self.estado = 'agotado'
            self.save()
            return True
        return False
    
    def aumentar_stock(self, cantidad):
        self.stock_cantidad += cantidad
        if self.estado == 'agotado' and self.stock_cantidad > 0:
            self.estado = 'disponible'
        self.save()
    
    def get_absolute_url(self):
        return reverse('productos:detalle', kwargs={'pk': self.pk})
    
    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.nombre}"


class ImagenProducto(models.Model):
    
    producto = models.ForeignKey(
        ProductosElectronicos, 
        on_delete=models.CASCADE,
        related_name='imagenes'
    )
    imagen = models.ImageField(upload_to='productos/imagenes/')
    alt_text = models.CharField(max_length=255, blank=True)
    es_principal = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=0)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'imagen_producto'
        verbose_name = 'Imagen de Producto'
        verbose_name_plural = 'Imágenes de Productos'
        ordering = ['orden', 'fecha_subida']
    
    def save(self, *args, **kwargs):
        # Asegurar que solo una imagen sea principal por producto
        if self.es_principal:
            ImagenProducto.objects.filter(
                producto=self.producto, 
                es_principal=True
            ).exclude(id=self.id).update(es_principal=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Imagen de {self.producto.nombre}"


class ResenaProducto(models.Model):
    
    producto = models.ForeignKey(
        ProductosElectronicos, 
        on_delete=models.CASCADE,
        related_name='resenas'
    )
    usuario = models.ForeignKey(
        UsuarioTienda, 
        on_delete=models.CASCADE,
        related_name='resenas'
    )
    calificacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(blank=True)
    fecha_resena = models.DateTimeField(auto_now_add=True)
    aprobada = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'resena_producto'
        verbose_name = 'Reseña de Producto'
        verbose_name_plural = 'Reseñas de Productos'
        unique_together = ['producto', 'usuario']
        ordering = ['-fecha_resena']
    
    def __str__(self):
        return f"Reseña de {self.usuario.username} para {self.producto.nombre}"





