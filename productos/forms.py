from django import forms
from .models import Review, CartItem, Producto, Categoria, ProductoCategoria


class ReviewForm(forms.ModelForm):
    """Formulario para crear/editar reseñas de productos"""
    
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{"⭐" * i}') for i in range(1, 6)],
                attrs={
                    'class': 'form-select',
                }
            ),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de tu reseña',
                'maxlength': 200
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Comparte tu experiencia con este producto...'
            }),
        }
        labels = {
            'rating': 'Calificación',
            'title': 'Título',
            'comment': 'Comentario'
        }


class CartItemForm(forms.ModelForm):
    """Formulario para agregar/actualizar items del carrito"""
    
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'value': 1
            })
        }
        labels = {
            'quantity': 'Cantidad'
        }


class ProductSearchForm(forms.Form):
    """Formulario de búsqueda avanzada de productos"""
    
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar productos...'
        }),
        label='Búsqueda'
    )
    
    categoria = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Categoría'
    )
    
    precio_min = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Precio mínimo',
            'step': '0.01'
        }),
        label='Precio Mínimo'
    )
    
    precio_max = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Precio máximo',
            'step': '0.01'
        }),
        label='Precio Máximo'
    )
    
    disponible = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Solo productos disponibles'
    )
    
    order_by = forms.ChoiceField(
        required=False,
        choices=[
            ('nombre', 'Nombre (A-Z)'),
            ('-nombre', 'Nombre (Z-A)'),
            ('precio', 'Precio (menor a mayor)'),
            ('-precio', 'Precio (mayor a menor)'),
            ('-fecha_creacion', 'Más recientes'),
            ('fecha_creacion', 'Más antiguos'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Ordenar por'
    )
    
    def __init__(self, *args, **kwargs):
        categorias = kwargs.pop('categorias', None)
        super().__init__(*args, **kwargs)
        
        if categorias:
            choices = [('', 'Todas las categorías')]
            choices.extend([(cat.id, cat.nombre) for cat in categorias])
            self.fields['categoria'].choices = choices


class ProductoForm(forms.ModelForm):
    """Formulario para crear/editar productos"""
    
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Categorías'
    )
    
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto',
                'maxlength': 100
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada del producto'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'precio': 'Precio',
            'stock': 'Stock'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Si estamos editando, seleccionar las categorías actuales
            self.fields['categorias'].initial = self.instance.categorias.values_list('categoria_id', flat=True)
    
    def save(self, commit=True):
        producto = super().save(commit=commit)
        if commit:
            # Eliminar categorías anteriores
            ProductoCategoria.objects.filter(producto=producto).delete()
            # Agregar las nuevas categorías
            for categoria in self.cleaned_data['categorias']:
                ProductoCategoria.objects.create(producto=producto, categoria=categoria)
        return producto


class CategoriaForm(forms.ModelForm):
    """Formulario para crear/editar categorías"""
    
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría',
                'maxlength': 100
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la categoría'
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción'
        }
