from django.contrib import admin
from .models import (
    Usuario, Producto, Categoria, ProductoCategoria, Pedido, DetallePedido, Reseña,
    Review, Favorite, ActivityLog, Notification, Cart, CartItem
)


# Configuración del modelo Usuario en el admin
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'fecha_registro')
    search_fields = ('nombre', 'email')
    list_filter = ('fecha_registro',)
    ordering = ('-fecha_registro',)
    readonly_fields = ('fecha_registro',)


# Configuración del modelo Producto en el admin
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'stock', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('fecha_creacion',)
    ordering = ('-fecha_creacion',)
    readonly_fields = ('fecha_creacion',)
    list_per_page = 20


# Configuración del modelo Categoria en el admin
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)


# Configuración del modelo ProductoCategoria en el admin
@admin.register(ProductoCategoria)
class ProductoCategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'categoria')
    search_fields = ('producto__nombre', 'categoria__nombre')
    list_filter = ('categoria',)
    autocomplete_fields = ['producto', 'categoria']


# Inline para DetallePedido en Pedido
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1
    fields = ('producto', 'cantidad', 'precio_unitario')


# Configuración del modelo Pedido en el admin
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha_pedido', 'total')
    search_fields = ('usuario__nombre', 'usuario__email')
    list_filter = ('fecha_pedido',)
    ordering = ('-fecha_pedido',)
    readonly_fields = ('fecha_pedido',)
    inlines = [DetallePedidoInline]


# Configuración del modelo DetallePedido en el admin
@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'producto', 'cantidad', 'precio_unitario')
    search_fields = ('pedido__id', 'producto__nombre')
    list_filter = ('pedido__fecha_pedido',)


# Configuración del modelo Reseña en el admin
@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'usuario', 'calificacion', 'fecha_reseña')
    search_fields = ('producto__nombre', 'usuario__nombre', 'comentario')
    list_filter = ('calificacion', 'fecha_reseña')
    ordering = ('-fecha_reseña',)
    readonly_fields = ('fecha_reseña',)


# Configuración del modelo Review en el admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'user', 'rating', 'title', 'is_verified_purchase', 'created_at')
    search_fields = ('producto__nombre', 'user__username', 'user__email', 'title', 'comment')
    list_filter = ('rating', 'is_verified_purchase', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'helpful_count')
    list_per_page = 20


# Configuración del modelo Favorite en el admin
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'producto', 'created_at')
    search_fields = ('user__username', 'user__email', 'producto__nombre')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


# Configuración del modelo ActivityLog en el admin
@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'activity_type', 'producto', 'created_at')
    search_fields = ('user__username', 'description', 'producto__nombre')
    list_filter = ('activity_type', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    list_per_page = 50


# Configuración del modelo Notification en el admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'notification_type', 'title', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    list_filter = ('notification_type', 'is_read', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    list_per_page = 50
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Marcar como leídas"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Marcar como no leídas"


# Inline para CartItem en Cart
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('producto', 'quantity', 'added_at')
    readonly_fields = ('added_at',)


# Configuración del modelo Cart en el admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_items', 'total_price', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-updated_at',)
    readonly_fields = ('created_at', 'updated_at', 'total_items', 'total_price')
    inlines = [CartItemInline]


# Configuración del modelo CartItem en el admin
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'producto', 'quantity', 'subtotal', 'added_at')
    search_fields = ('cart__user__username', 'producto__nombre')
    list_filter = ('added_at',)
    ordering = ('-added_at',)
    readonly_fields = ('added_at', 'subtotal')

