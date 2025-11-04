"""
URLs de la aplicación productos.

Define las rutas para:
- Página de inicio
- Lista de productos
- Detalle de producto
- Lista de categorías
- Productos por categoría
- Reseñas
- Favoritos
- Carrito de compras
- Notificaciones
- Búsqueda avanzada
"""

from django.urls import path
from . import views, views_features, views_crud

app_name = 'productos'

urlpatterns = [
    # Página de inicio
    path('', views.inicio, name='inicio'),
    
    # CRUD Productos (Admin)
    path('productos/', views_crud.producto_list, name='producto_list'),
    path('productos/crear/', views_crud.producto_create, name='producto_create'),
    path('productos/<int:pk>/', views_crud.producto_detail, name='producto_detail'),
    path('productos/<int:pk>/editar/', views_crud.producto_update, name='producto_update'),
    path('productos/<int:pk>/eliminar/', views_crud.producto_delete, name='producto_delete'),
    
    # CRUD Categorías (Admin)
    path('categorias/', views_crud.categoria_list, name='categoria_list'),
    path('categorias/crear/', views_crud.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/', views_crud.categoria_detail, name='categoria_detail'),
    path('categorias/<int:pk>/editar/', views_crud.categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', views_crud.categoria_delete, name='categoria_delete'),
    
    # Búsqueda
    path('buscar/', views_features.search_products, name='search_products'),
    
    # Reseñas
    path('productos/<int:producto_id>/review/crear/', views_features.create_review, name='create_review'),
    path('review/<int:review_id>/editar/', views_features.edit_review, name='edit_review'),
    path('review/<int:review_id>/eliminar/', views_features.delete_review, name='delete_review'),
    path('mis-reviews/', views_features.my_reviews, name='my_reviews'),
    
    # Favoritos
    path('productos/<int:producto_id>/favorito/', views_features.toggle_favorite, name='toggle_favorite'),
    path('mis-favoritos/', views_features.my_favorites, name='my_favorites'),
    
    # Carrito
    path('carrito/', views_features.view_cart, name='view_cart'),
    path('carrito/agregar/<int:producto_id>/', views_features.add_to_cart, name='add_to_cart'),
    path('carrito/actualizar/<int:item_id>/', views_features.update_cart_item, name='update_cart_item'),
    path('carrito/remover/<int:item_id>/', views_features.remove_from_cart, name='remove_from_cart'),
    path('carrito/vaciar/', views_features.clear_cart, name='clear_cart'),
    
    # Notificaciones
    path('notificaciones/', views_features.my_notifications, name='my_notifications'),
    path('notificaciones/<int:notification_id>/leer/', views_features.mark_notification_read, name='mark_notification_read'),
    
    # Actividad
    path('mi-actividad/', views_features.my_activity, name='my_activity'),
]

