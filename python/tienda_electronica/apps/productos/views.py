
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from .models import ProductosElectronicos, CategoriaProducto, ImagenProducto, ResenaProducto
from .forms import ProductoForm, ImagenProductoForm, ResenaForm
import django_filters

class ListaProductosView(ListView):
    model = ProductosElectronicos
    template_name = 'productos/lista_productos.html'
    context_object_name = 'productos'
    paginate_by = 12

    def get_queryset(self):
        queryset = ProductosElectronicos.objects.filter(estado='disponible')

        # Filtrar por categoría (usando ID)
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)

        # Búsqueda por texto
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(marca__icontains=query) |
                Q(modelo__icontains=query) |
                Q(descripcion__icontains=query)
            )

        # Filtro personalizado (como django-filter)
        self.filtro = ProductoFilter(self.request.GET, queryset=queryset)
        return self.filtro.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtro'] = self.filtro
        context['categorias'] = CategoriaProducto.objects.filter(activa=True)
        context['productos_destacados'] = ProductosElectronicos.objects.filter(
            destacado=True, estado='disponible'
        )[:4]

        # Mantener el filtro actual (útil para paginación con filtros)
        context['categoria_id'] = self.request.GET.get('categoria', '')
        context['query'] = self.request.GET.get('q', '')
        return context

def inicio(request):
    productos_destacados = ProductosElectronicos.objects.filter(
        destacado=True, stock_cantidad__gt=0
    )[:6]
    return render(request, 'productos/inicio.html', {'productos': productos_destacados})

class DetalleProductoView(DetailView):
    model = ProductosElectronicos
    template_name = 'productos/detalle_producto.html'
    context_object_name = 'producto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        producto = self.object
        
        context['resenas'] = producto.resenas.filter(aprobada=True)
        context['promedio_calificacion'] = producto.resenas.filter(
            aprobada=True
        ).aggregate(Avg('calificacion'))['calificacion__avg']
        
        context['productos_relacionados'] = ProductosElectronicos.objects.filter(
            categoria=producto.categoria,
            estado='disponible'
        ).exclude(id=producto.id)[:4]
        
        # Formulario de reseña
        if self.request.user.is_authenticated:
            context['form_resena'] = ResenaForm()
        
        return context


class CrearProductoView(LoginRequiredMixin, CreateView):
    model = ProductosElectronicos
    form_class = ProductoForm
    template_name = 'productos/crear_producto.html'
    success_url = reverse_lazy('productos:lista')
    
    def form_valid(self, form):
        form.instance.usuario_creador = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Producto creado exitosamente')
        return response


class EditarProductoView(LoginRequiredMixin, UpdateView):
    model = ProductosElectronicos
    form_class = ProductoForm
    template_name = 'productos/editar_producto.html'
    
    def get_success_url(self):
        return reverse_lazy('productos:detalle', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Producto actualizado exitosamente')
        return response


class EliminarProductoView(LoginRequiredMixin, DeleteView):
    model = ProductosElectronicos
    template_name = 'productos/confirmar_eliminacion.html'
    success_url = reverse_lazy('productos:lista')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Producto eliminado exitosamente')
        return super().delete(request, *args, **kwargs)


@login_required
def agregar_resena(request, producto_id):
    producto = get_object_or_404(ProductosElectronicos, id=producto_id)
    
    if request.method == 'POST':
        form = ResenaForm(request.POST)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.producto = producto
            resena.usuario = request.user
            resena.save()
            messages.success(request, 'Reseña agregada exitosamente')
            return redirect('productos:detalle', pk=producto.pk)
    
    return redirect('productos:detalle', pk=producto.pk)


def productos_por_categoria(request, slug):
    categoria = get_object_or_404(CategoriaProducto, slug=slug, activa=True)
    productos = ProductosElectronicos.objects.filter(
        categoria=categoria,
        estado='disponible'
    )
    
    paginator = Paginator(productos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categoria_actual': categoria,
        'productos': page_obj,
        'categorias': CategoriaProducto.objects.filter(activa=True),
    }
    
    return render(request, 'productos/productos_categorias.html', context)

class ProductoFilter(django_filters.FilterSet):
    class Meta:
        model = ProductosElectronicos
        fields = {
            'nombre': ['icontains'],  
            'precio': ['lt', 'gt'],   
            'categoria': ['exact'],   
        }
        
@login_required
@require_POST
def toggle_favorito_ajax(request):
    producto_id = request.POST.get('producto_id')
    user = request.user

    try:
        producto = ProductosElectronicos.objects.get(id=producto_id)
    except ProductosElectronicos.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

    if producto in user.productos_favoritos.all():
        user.productos_favoritos.remove(producto)
        favorito = False
    else:
        user.productos_favoritos.add(producto)
        favorito = True

    return JsonResponse({'favorito': favorito})

@login_required
def lista_favoritos(request):
    favoritos = request.user.productos_favoritos.all()
    return render(request, 'productos/favoritos.html', {'favoritos': favoritos})

