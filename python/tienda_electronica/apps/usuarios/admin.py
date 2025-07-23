from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioTienda

@admin.register(UsuarioTienda)
class UsuarioTiendaAdmin(UserAdmin):
    list_display=('username','email','first_name','last_name','is_admin','fecha_registro')
    list_filter=('is_admin','is_active','fecha_registro')
    search_fields=('username','email','first_name','last_name')

    fieldsets=UserAdmin.fieldsets+(('Informacion adicional',{
        'fields':('telefono','direccion','avatar','is_admin','f_ultimo_ingreso')
    }),
    )

    readonly_fields=('fecha_registro','f_ultimo_ingreso')
