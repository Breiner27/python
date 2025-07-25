from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Autenticación
    path('registro/', views.RegistroUsuarioView.as_view(), name='registro'),
    path('login/', views.login_vista, name='login'),
    path('logout/', views.logout_vista, name='logout'),
    
    # Dashboard y perfil
    path('dashboard/', views.dashboard_vista, name='dashboard'),
    path('perfil/', views.perfil_vista, name='perfil'),
    path('perfil/editar/', views.actualizar_perfil_vista, name='actualizar_perfil'),
    
    # Cambio de contraseña (usando vistas built-in de Django)
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='usuarios/password_change.html',
        success_url='/usuarios/perfil/'
    ), name='password_change'),
    
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='usuarios/password_change_done.html'
    ), name='password_change_done'),
]