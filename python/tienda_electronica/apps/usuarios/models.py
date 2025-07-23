from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class UsuarioTienda(AbstractUser):
    telefono=models.CharField(max_length=10,blank=True)
    direccion=models.TextField(blank=True)
    fecha_registro=models.DateTimeField(auto_now_add=True)
    f_ultimo_ingreso=models.DateTimeField(null=True,blank=True)
    is_admin=models.BooleanField(default=False)
    avatar=models.ImageField(upload_to='usuarios/avatares/',blank=True)
    productos_favoritos = models.ManyToManyField(
    'productos.ProductosElectronicos',
    blank=True,
    related_name='usuarios_que_favoritan'
)


    class Meta:
        db_table='electronicos'
        verbose_name='Usuario'
        verbose_name_plural='Usuarios'

    def actualizar_acceso(self):
        self.f_ultimo_ingreso=timezone.now()
        self.save(update_fields=['f_ultimo_ingreso'])

    def __str__(self):
        return f"{self.first_name}{self.last_name} ({self.username})"
    
