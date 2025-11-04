"""
Vistas CRUD para Productos y Categorías
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count
from .models import Producto, Categoria, ProductoCategoria
from .forms import ProductoForm, CategoriaForm


def is_admin(user):
    """Verifica si el usuario es administrador"""
    return user.is_staff or user.is_superuser


# ============================================
# CRUD de Productos
# ============================================

def producto_list(request):
    """Lista todos los productos"""
    productos = Producto.objects.all().order_by('-fecha_creacion')
    
    # Búsqueda simple
    query = request.GET.get('q', '')
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | 
            Q(descripcion__icontains=query)
        )
    
    context = {
        'productos': productos,
        'query': query,
    }
    return render(request, 'productos/producto_list.html', context)


@login_required
@user_passes_test(is_admin)
def producto_create(request):
    """Crear un nuevo producto"""
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
            return redirect('productos:producto_detail', pk=producto.pk)
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = ProductoForm()
    
    context = {
        'form': form,
        'title': 'Crear Producto',
        'button_text': 'Crear Producto'
    }
    return render(request, 'productos/producto_form.html', context)


def producto_detail(request, pk):
    """Detalle de un producto"""
    producto = get_object_or_404(Producto, pk=pk)
    categorias = producto.categorias.all()
    
    # Obtener productos relacionados (de las mismas categorías)
    if categorias:
        categoria_ids = categorias.values_list('categoria_id', flat=True)
        productos_relacionados = Producto.objects.filter(
            categorias__categoria_id__in=categoria_ids
        ).exclude(pk=producto.pk).distinct()[:4]
    else:
        productos_relacionados = []
    
    context = {
        'producto': producto,
        'categorias': categorias,
        'productos_relacionados': productos_relacionados,
    }
    return render(request, 'productos/producto_detail.html', context)


@login_required
@user_passes_test(is_admin)
def producto_update(request, pk):
    """Actualizar un producto existente"""
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
            return redirect('productos:producto_detail', pk=producto.pk)
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = ProductoForm(instance=producto)
    
    context = {
        'form': form,
        'producto': producto,
        'title': f'Editar Producto: {producto.nombre}',
        'button_text': 'Actualizar Producto'
    }
    return render(request, 'productos/producto_form.html', context)


@login_required
@user_passes_test(is_admin)
def producto_delete(request, pk):
    """Eliminar un producto"""
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado exitosamente.')
        return redirect('productos:producto_list')
    
    context = {
        'producto': producto,
    }
    return render(request, 'productos/producto_confirm_delete.html', context)


# ============================================
# CRUD de Categorías
# ============================================

def categoria_list(request):
    """Lista todas las categorías"""
    categorias = Categoria.objects.annotate(
        num_productos=Count('productos')
    ).order_by('nombre')
    
    context = {
        'categorias': categorias,
    }
    return render(request, 'productos/categoria_list.html', context)


@login_required
@user_passes_test(is_admin)
def categoria_create(request):
    """Crear una nueva categoría"""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" creada exitosamente.')
            return redirect('productos:categoria_list')
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = CategoriaForm()
    
    context = {
        'form': form,
        'title': 'Crear Categoría',
        'button_text': 'Crear Categoría'
    }
    return render(request, 'productos/categoria_form.html', context)


def categoria_detail(request, pk):
    """Detalle de una categoría con sus productos"""
    categoria = get_object_or_404(Categoria, pk=pk)
    productos = Producto.objects.filter(
        categorias__categoria=categoria
    ).distinct().order_by('-fecha_creacion')
    
    context = {
        'categoria': categoria,
        'productos': productos,
    }
    return render(request, 'productos/categoria_detail.html', context)


@login_required
@user_passes_test(is_admin)
def categoria_update(request, pk):
    """Actualizar una categoría existente"""
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" actualizada exitosamente.')
            return redirect('productos:categoria_list')
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = CategoriaForm(instance=categoria)
    
    context = {
        'form': form,
        'categoria': categoria,
        'title': f'Editar Categoría: {categoria.nombre}',
        'button_text': 'Actualizar Categoría'
    }
    return render(request, 'productos/categoria_form.html', context)


@login_required
@user_passes_test(is_admin)
def categoria_delete(request, pk):
    """Eliminar una categoría"""
    categoria = get_object_or_404(Categoria, pk=pk)
    num_productos = categoria.productos.count()
    
    if request.method == 'POST':
        nombre = categoria.nombre
        categoria.delete()
        messages.success(request, f'Categoría "{nombre}" eliminada exitosamente.')
        return redirect('productos:categoria_list')
    
    context = {
        'categoria': categoria,
        'num_productos': num_productos,
    }
    return render(request, 'productos/categoria_confirm_delete.html', context)
