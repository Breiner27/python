# views.py - Actualización recomendada
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Sum, Count
from .models import UsuarioTienda
from .forms import RegistroUsuariosForm, ActualizarPerfilForms
from django.views.decorators.cache import never_cache

class RegistroUsuarioView(CreateView):
    model = UsuarioTienda
    form_class = RegistroUsuariosForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('usuarios:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.first_name = form.cleaned_data.get('Nombres')
        user.last_name = form.cleaned_data.get('Apellidos')
        user.save()
        
        messages.success(self.request, 'Cuenta creada exitosamente. ¡Inicia sesión!')
        return redirect(self.success_url)

def login_vista(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            user.actualizar_acceso()
            
            if user.is_superuser or user.is_staff:
                return redirect('/admin/')

            messages.success(request, f'¡Bienvenido, {user.first_name or user.username}!')
            return redirect('productos:inicio')
        else:
            messages.error(request, 'Credenciales inválidas')
    
    return render(request, 'usuarios/login.html')

@login_required
@never_cache
def dashboard_vista(request):
    usuario = request.user
    
    total_pedidos = 0
    total_gastado = 0
    productos_favoritos = 0
    
    
    context = {
        'usuario': usuario,
        'total_pedidos': total_pedidos,
        'total_gastado': total_gastado,
        'productos_favoritos': productos_favoritos,
    }
    return render(request, 'usuarios/dashboard.html', context)

@login_required
def perfil_vista(request):
    total_gastado = request.user.pedidos.aggregate(total_gastado=Sum('total'))['total_gastado'] or 0

    if request.method == 'POST':
        form = ActualizarPerfilForms(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('usuarios:perfil')  
    else:
        form = ActualizarPerfilForms(instance=request.user)

    context = {
        'form': form,
        'usuario': request.user,
        'total_gastado': total_gastado,
    }
    return render(request, 'usuarios/profile.html', context)


@login_required
def actualizar_perfil_vista(request):
    if request.method == 'POST':
        form = ActualizarPerfilForms(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('usuarios:perfil')
    else:
        form = ActualizarPerfilForms(instance=request.user)

    return render(request, 'usuarios/actualizar_perfil.html', {'form': form})

def logout_vista(request):
    logout(request)
    messages.info(request, 'Sesión cerrada exitosamente')
    return redirect('productos:inicio')