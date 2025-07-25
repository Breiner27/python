from django import forms
from .models import ProductosElectronicos, ImagenProducto, ResenaProducto, CategoriaProducto
from . import views

class ProductoForm(forms.ModelForm):
    class Meta:
        model = ProductosElectronicos
        fields = [
            'nombre', 'descripcion', 'precio', 'precio_oferta', 'stock_cantidad',
            'stock_minimo', 'sku', 'marca', 'modelo', 'color', 'peso',
            'dimensiones', 'categoria', 'destacado', 'especificaciones_tecnicas'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_oferta': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
            'dimensiones': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'destacado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'especificaciones_tecnicas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = CategoriaProducto.objects.filter(activa=True)


class ImagenProductoForm(forms.ModelForm):
    class Meta:
        model = ImagenProducto
        fields = ['imagen', 'alt_text', 'es_principal', 'orden']
        widgets = {
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'alt_text': forms.TextInput(attrs={'class': 'form-control'}),
            'es_principal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ResenaForm(forms.ModelForm):
    class Meta:
        model = ResenaProducto
        fields = ['calificacion', 'comentario']
        widgets = {
            'calificacion': forms.Select(
                choices=[(i, f'{i} estrella{"s" if i > 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'form-control'}
            ),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }



import django_filters


class ProductoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(
        field_name='nombre',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar producto...'})
    )
    
    marca = django_filters.CharFilter(
        field_name='marca',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca...'})
    )
    
    categoria = django_filters.ModelChoiceFilter(
        queryset=CategoriaProducto.objects.filter(activa=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    precio_min = django_filters.NumberFilter(
        field_name='precio',
        lookup_expr='gte',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio mínimo'})
    )
    
    precio_max = django_filters.NumberFilter(
        field_name='precio',
        lookup_expr='lte',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio máximo'})
    )
    
    destacado = django_filters.BooleanFilter(
        field_name='destacado',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = ProductosElectronicos
        fields = ['nombre', 'marca', 'categoria', 'precio_min', 'precio_max', 'destacado']
