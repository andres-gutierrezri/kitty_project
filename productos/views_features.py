from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg, Count
from django.views.decorators.http import require_POST
from .models import (
    Producto, Review, Favorite, ActivityLog, 
    Notification, Cart, CartItem, Categoria
)
from .forms import ReviewForm, CartItemForm, ProductSearchForm


# ============================================
# VISTAS DE RESEÑAS
# ============================================

@login_required
def create_review(request, producto_id):
    """Vista para crear una reseña de producto"""
    producto = get_object_or_404(Producto, pk=producto_id)
    
    # Verificar si el usuario ya ha hecho una reseña
    existing_review = Review.objects.filter(producto=producto, user=request.user).first()
    if existing_review:
        messages.warning(request, 'Ya has escrito una reseña para este producto.')
        return redirect('productos:producto_detail', pk=producto_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.producto = producto
            review.user = request.user
            review.save()
            
            # Registrar actividad
            ActivityLog.objects.create(
                user=request.user,
                activity_type='review',
                producto=producto,
                description=f'Escribió una reseña para {producto.nombre}'
            )
            
            messages.success(request, '¡Reseña publicada exitosamente!')
            return redirect('productos:producto_detail', pk=producto_id)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'producto': producto,
    }
    return render(request, 'productos/create_review.html', context)


@login_required
def edit_review(request, review_id):
    """Vista para editar una reseña existente"""
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reseña actualizada exitosamente.')
            return redirect('productos:producto_detail', pk=review.producto.pk)
    else:
        form = ReviewForm(instance=review)
    
    context = {
        'form': form,
        'review': review,
        'producto': review.producto,
    }
    return render(request, 'productos/edit_review.html', context)


@login_required
@require_POST
def delete_review(request, review_id):
    """Vista para eliminar una reseña"""
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    producto_id = review.producto.pk
    review.delete()
    messages.success(request, 'Reseña eliminada exitosamente.')
    return redirect('productos:producto_detail', pk=producto_id)


@login_required
def my_reviews(request):
    """Vista para mostrar las reseñas del usuario"""
    reviews = Review.objects.filter(user=request.user).select_related('producto').order_by('-created_at')
    
    context = {
        'reviews': reviews,
    }
    return render(request, 'productos/my_reviews.html', context)


# ============================================
# VISTAS DE FAVORITOS
# ============================================

@login_required
@require_POST
def toggle_favorite(request, producto_id):
    """Vista para agregar/quitar producto de favoritos"""
    producto = get_object_or_404(Producto, pk=producto_id)
    
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        producto=producto
    )
    
    if created:
        # Registrar actividad
        ActivityLog.objects.create(
            user=request.user,
            activity_type='favorite',
            producto=producto,
            description=f'Agregó {producto.nombre} a favoritos'
        )
        messages.success(request, f'{producto.nombre} agregado a favoritos.')
        favorited = True
    else:
        favorite.delete()
        # Registrar actividad
        ActivityLog.objects.create(
            user=request.user,
            activity_type='unfavorite',
            producto=producto,
            description=f'Removió {producto.nombre} de favoritos'
        )
        messages.info(request, f'{producto.nombre} removido de favoritos.')
        favorited = False
    
    # Si es una petición AJAX, devolver JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'favorited': favorited})
    
    return redirect('productos:producto_detail', pk=producto_id)


@login_required
def my_favorites(request):
    """Vista para mostrar los productos favoritos del usuario"""
    favorites = Favorite.objects.filter(user=request.user).select_related('producto').order_by('-created_at')
    
    context = {
        'favorites': favorites,
    }
    return render(request, 'productos/my_favorites.html', context)


# ============================================
# VISTAS DE CARRITO
# ============================================

@login_required
def view_cart(request):
    """Vista para mostrar el carrito de compras"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('producto').all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'productos/cart.html', context)


@login_required
@require_POST
def add_to_cart(request, producto_id):
    """Vista para agregar producto al carrito"""
    producto = get_object_or_404(Producto, pk=producto_id)
    quantity = int(request.POST.get('quantity', 1))
    
    # Validar stock
    if quantity > producto.stock:
        messages.error(request, f'Solo hay {producto.stock} unidades disponibles.')
        return redirect('productos:producto_detail', pk=producto_id)
    
    # Obtener o crear carrito
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Agregar o actualizar item
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        producto=producto,
        defaults={'quantity': quantity}
    )
    
    if not item_created:
        cart_item.quantity += quantity
        if cart_item.quantity > producto.stock:
            messages.error(request, f'Solo hay {producto.stock} unidades disponibles.')
            return redirect('productos:view_cart')
        cart_item.save()
    
    # Registrar actividad
    ActivityLog.objects.create(
        user=request.user,
        activity_type='cart_add',
        producto=producto,
        description=f'Agregó {quantity} unidad(es) de {producto.nombre} al carrito'
    )
    
    messages.success(request, f'{producto.nombre} agregado al carrito.')
    
    # Si es AJAX, devolver JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.total_items
        })
    
    return redirect('productos:view_cart')


@login_required
@require_POST
def update_cart_item(request, item_id):
    """Vista para actualizar cantidad de un item del carrito"""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart_item.delete()
        messages.info(request, 'Producto removido del carrito.')
    elif quantity > cart_item.producto.stock:
        messages.error(request, f'Solo hay {cart_item.producto.stock} unidades disponibles.')
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Carrito actualizado.')
    
    return redirect('productos:view_cart')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Vista para remover item del carrito"""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    producto_nombre = cart_item.producto.nombre
    cart_item.delete()
    messages.info(request, f'{producto_nombre} removido del carrito.')
    return redirect('productos:view_cart')


@login_required
@require_POST
def clear_cart(request):
    """Vista para vaciar el carrito"""
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    messages.info(request, 'Carrito vaciado.')
    return redirect('productos:view_cart')


# ============================================
# VISTAS DE NOTIFICACIONES
# ============================================

@login_required
def my_notifications(request):
    """Vista para mostrar las notificaciones del usuario"""
    # Primero marcamos como leídas las no leídas
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    # Luego obtenemos las notificaciones (ya están marcadas como leídas)
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:50]
    
    context = {
        'notifications': notifications,
    }
    return render(request, 'productos/notifications.html', context)


@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """Vista para marcar una notificación como leída"""
    notification = get_object_or_404(Notification, pk=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('productos:my_notifications')


# ============================================
# VISTAS DE BÚSQUEDA AVANZADA
# ============================================

def search_products(request):
    """Vista de búsqueda avanzada de productos"""
    categorias = Categoria.objects.all()
    form = ProductSearchForm(request.GET or None, categorias=categorias)
    
    productos = Producto.objects.all()
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        categoria = form.cleaned_data.get('categoria')
        precio_min = form.cleaned_data.get('precio_min')
        precio_max = form.cleaned_data.get('precio_max')
        disponible = form.cleaned_data.get('disponible')
        order_by = form.cleaned_data.get('order_by')
        
        # Aplicar filtros
        if query:
            productos = productos.filter(
                Q(nombre__icontains=query) |
                Q(descripcion__icontains=query)
            )
        
        if categoria:
            productos = productos.filter(categorias__categoria_id=categoria).distinct()
        
        if precio_min is not None:
            productos = productos.filter(precio__gte=precio_min)
        
        if precio_max is not None:
            productos = productos.filter(precio__lte=precio_max)
        
        if disponible:
            productos = productos.filter(stock__gt=0)
        
        if order_by:
            productos = productos.order_by(order_by)
    
    # Agregar información adicional
    productos = productos.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    )
    
    context = {
        'form': form,
        'productos': productos,
        'total_results': productos.count(),
    }
    return render(request, 'productos/search.html', context)


# ============================================
# VISTA DE ACTIVIDAD (para el dashboard)
# ============================================

@login_required
def my_activity(request):
    """Vista para mostrar el historial de actividad del usuario"""
    activities = ActivityLog.objects.filter(user=request.user).select_related('producto').order_by('-created_at')[:50]
    
    context = {
        'activities': activities,
    }
    return render(request, 'productos/my_activity.html', context)
