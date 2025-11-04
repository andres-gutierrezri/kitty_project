from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your models here.

# Modelo Usuario
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_registro']

    def __str__(self):
        return self.nombre

    def clean(self):
        """Validación personalizada para el modelo Usuario"""
        super().clean()
        if self.nombre and len(self.nombre.strip()) < 2:
            raise ValidationError({'nombre': 'El nombre debe tener al menos 2 caracteres.'})


# Modelo Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01, message='El precio debe ser mayor a 0')]
    )
    stock = models.IntegerField(
        validators=[MinValueValidator(0, message='El stock no puede ser negativo')]
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.nombre

    def clean(self):
        """Validación personalizada para el modelo Producto"""
        super().clean()
        if self.nombre and len(self.nombre.strip()) < 3:
            raise ValidationError({'nombre': 'El nombre del producto debe tener al menos 3 caracteres.'})
        if self.descripcion and len(self.descripcion.strip()) < 10:
            raise ValidationError({'descripcion': 'La descripción debe tener al menos 10 caracteres.'})

    @property
    def disponible(self):
        """Verifica si el producto está disponible en stock"""
        return self.stock > 0
    
# Modelo Pedido
class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0, message='El total no puede ser negativo')]
    )

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_pedido']

    def __str__(self):
        return f'Pedido {self.id} - Usuario: {self.usuario.nombre}'
    
# Modelo DetallePedido
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='detalles_pedido')
    cantidad = models.IntegerField(
        validators=[MinValueValidator(1, message='La cantidad debe ser al menos 1')]
    )
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01, message='El precio unitario debe ser mayor a 0')]
    )

    class Meta:
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalles de Pedidos'

    def __str__(self):
        return f'Detalle del Pedido {self.pedido.id} - Producto: {self.producto.nombre}'

    @property
    def subtotal(self):
        """Calcula el subtotal de la línea de pedido"""
        return self.cantidad * self.precio_unitario
    
# Modelo Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def clean(self):
        """Validación personalizada para el modelo Categoria"""
        super().clean()
        if self.nombre and len(self.nombre.strip()) < 3:
            raise ValidationError({'nombre': 'El nombre de la categoría debe tener al menos 3 caracteres.'})


# Relación muchos a muchos entre Producto y Categoria
class ProductoCategoria(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='categorias')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')

    class Meta:
        verbose_name = 'Producto-Categoría'
        verbose_name_plural = 'Productos-Categorías'
        unique_together = ('producto', 'categoria')  # Evitar duplicados

    def __str__(self):
        return f'Producto: {self.producto.nombre} - Categoria: {self.categoria.nombre}'
    
# Modelo Reseña
class Reseña(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='reseñas')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reseñas')
    calificacion = models.IntegerField(
        validators=[
            MinValueValidator(1, message='La calificación mínima es 1'),
            MaxValueValidator(5, message='La calificación máxima es 5')
        ]
    )
    comentario = models.TextField()
    fecha_reseña = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'
        ordering = ['-fecha_reseña']
        unique_together = ('producto', 'usuario')  # Un usuario solo puede reseñar un producto una vez

    def __str__(self):
        return f'Reseña de {self.usuario.nombre} para {self.producto.nombre} - {self.calificacion}⭐'

    def clean(self):
        """Validación personalizada para el modelo Reseña"""
        super().clean()
        if self.comentario and len(self.comentario.strip()) < 10:
            raise ValidationError({'comentario': 'El comentario debe tener al menos 10 caracteres.'})


# Modelo Review (Sistema de reseñas mejorado para usuarios autenticados)
class Review(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1, message='La calificación mínima es 1'),
            MaxValueValidator(5, message='La calificación máxima es 5')
        ],
        verbose_name='Calificación'
    )
    title = models.CharField(max_length=200, verbose_name='Título')
    comment = models.TextField(verbose_name='Comentario')
    helpful_count = models.IntegerField(default=0, verbose_name='Votos útiles')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    is_verified_purchase = models.BooleanField(default=False, verbose_name='Compra verificada')

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
        unique_together = ('producto', 'user')

    def __str__(self):
        return f'Review de {self.user.get_full_name() or self.user.username} para {self.producto.nombre}'

    def clean(self):
        super().clean()
        if self.comment and len(self.comment.strip()) < 10:
            raise ValidationError({'comment': 'El comentario debe tener al menos 10 caracteres.'})
        if self.title and len(self.title.strip()) < 5:
            raise ValidationError({'title': 'El título debe tener al menos 5 caracteres.'})


# Modelo Favorite (Lista de favoritos)
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de agregado')

    class Meta:
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
        ordering = ['-created_at']
        unique_together = ('user', 'producto')

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} - {self.producto.nombre}'


# Modelo ActivityLog (Historial de actividad)
class ActivityLog(models.Model):
    ACTIVITY_TYPES = [
        ('view', 'Visualización de producto'),
        ('review', 'Reseña escrita'),
        ('favorite', 'Agregado a favoritos'),
        ('unfavorite', 'Removido de favoritos'),
        ('cart_add', 'Agregado al carrito'),
        ('purchase', 'Compra realizada'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES, verbose_name='Tipo de actividad')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True, related_name='activities')
    description = models.CharField(max_length=255, verbose_name='Descripción')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')

    class Meta:
        verbose_name = 'Registro de actividad'
        verbose_name_plural = 'Registros de actividad'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.get_activity_type_display()} - {self.created_at.strftime("%Y-%m-%d %H:%M")}'


# Modelo Notification (Sistema de notificaciones)
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('new_product', 'Nuevo producto'),
        ('price_drop', 'Bajada de precio'),
        ('review_reply', 'Respuesta a reseña'),
        ('favorite_available', 'Favorito disponible'),
        ('system', 'Sistema'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, verbose_name='Tipo')
    title = models.CharField(max_length=200, verbose_name='Título')
    message = models.TextField(verbose_name='Mensaje')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    is_read = models.BooleanField(default=False, verbose_name='Leída')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.user.username}'


# Modelo Cart (Carrito de compras)
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')

    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'

    def __str__(self):
        return f'Carrito de {self.user.get_full_name() or self.user.username}'

    @property
    def total_items(self):
        """Calcula el total de items en el carrito"""
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        """Calcula el precio total del carrito"""
        return sum(item.subtotal for item in self.items.all())


# Modelo CartItem (Items del carrito)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1, message='La cantidad debe ser al menos 1')],
        verbose_name='Cantidad'
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de agregado')

    class Meta:
        verbose_name = 'Item del carrito'
        verbose_name_plural = 'Items del carrito'
        unique_together = ('cart', 'producto')

    def __str__(self):
        return f'{self.producto.nombre} x {self.quantity}'

    @property
    def subtotal(self):
        """Calcula el subtotal del item"""
        return self.producto.precio * self.quantity

    def clean(self):
        super().clean()
        if self.quantity > self.producto.stock:
            raise ValidationError({
                'quantity': f'Solo hay {self.producto.stock} unidades disponibles.'
            })
    
