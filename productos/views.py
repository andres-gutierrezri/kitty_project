from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count
from .models import Producto, Categoria, ProductoCategoria, Reseña, Review, Favorite


def inicio(request):
    """
    Vista de la página de inicio.
    Muestra productos destacados y categorías principales.
    """
    # Obtener los últimos 6 productos agregados
    productos_recientes = Producto.objects.all().order_by('-fecha_creacion')[:6]
    
    # Obtener todas las categorías con conteo de productos
    categorias = Categoria.objects.annotate(
        num_productos=Count('productos')
    ).order_by('nombre')
    
    context = {
        'productos_recientes': productos_recientes,
        'categorias': categorias,
    }
    return render(request, 'productos/inicio.html', context)


def lista_productos(request):
    """
    Vista que muestra la lista completa de productos.
    Con información de stock y precio.
    """
    productos = Producto.objects.all().order_by('-fecha_creacion')
    
    # Filtro de búsqueda (opcional)
    busqueda = request.GET.get('q', '')
    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)
    
    context = {
        'productos': productos,
        'busqueda': busqueda,
    }
    return render(request, 'productos/lista_productos.html', context)


def detalle_producto(request, pk):
    """
    Vista que muestra los detalles de un producto específico.
    Incluye categorías, reseñas y calificación promedio.
    """
    producto = get_object_or_404(Producto, pk=pk)
    
    # Registrar visualización si el usuario está autenticado
    if request.user.is_authenticated:
        from .models import ActivityLog
        ActivityLog.objects.create(
            user=request.user,
            activity_type='view',
            producto=producto,
            description=f'Visualizó {producto.nombre}'
        )
    
    # Obtener categorías del producto
    categorias_producto = ProductoCategoria.objects.filter(
        producto=producto
    ).select_related('categoria')
    
    # Obtener reseñas antiguas del producto
    reseñas = Reseña.objects.filter(
        producto=producto
    ).select_related('usuario').order_by('-fecha_reseña')
    
    # Obtener nuevas reviews
    reviews = Review.objects.filter(
        producto=producto
    ).select_related('user').order_by('-created_at')
    
    # Calcular calificación promedio de reviews
    review_stats = reviews.aggregate(
        promedio=Avg('rating'),
        total=Count('id')
    )
    
    # Verificar si el usuario ha hecho review
    user_review = None
    is_favorited = False
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        is_favorited = Favorite.objects.filter(user=request.user, producto=producto).exists()
    
    context = {
        'producto': producto,
        'categorias': categorias_producto,
        'reseñas': reseñas,
        'reviews': reviews,
        'calificacion_promedio': review_stats['promedio'],
        'total_reviews': review_stats['total'],
        'user_review': user_review,
        'is_favorited': is_favorited,
    }
    return render(request, 'productos/producto_detail.html', context)


def lista_categorias(request):
    """
    Vista que muestra todas las categorías disponibles.
    Con conteo de productos por categoría.
    """
    categorias = Categoria.objects.annotate(
        num_productos=Count('productos')
    ).order_by('nombre')
    
    context = {
        'categorias': categorias,
    }
    return render(request, 'productos/lista_categorias.html', context)


def productos_por_categoria(request, pk):
    """
    Vista que muestra todos los productos de una categoría específica.
    """
    categoria = get_object_or_404(Categoria, pk=pk)
    
    # Obtener productos de esta categoría
    productos_categoria = ProductoCategoria.objects.filter(
        categoria=categoria
    ).select_related('producto')
    
    # Extraer los productos
    productos = [pc.producto for pc in productos_categoria]
    
    context = {
        'categoria': categoria,
        'productos': productos,
    }
    return render(request, 'productos/productos_por_categoria.html', context)

