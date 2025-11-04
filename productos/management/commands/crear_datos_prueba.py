"""
Script para crear datos de prueba: categorías y productos
"""
from django.core.management.base import BaseCommand
from productos.models import Categoria, Producto, ProductoCategoria


class Command(BaseCommand):
    help = 'Crea categorías y productos de prueba'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creando datos de prueba...'))
        
        # Crear categorías
        categorias_data = [
            {
                'nombre': 'Electrónica',
                'descripcion': 'Dispositivos electrónicos y accesorios tecnológicos'
            },
            {
                'nombre': 'Ropa',
                'descripcion': 'Prendas de vestir y accesorios de moda'
            },
            {
                'nombre': 'Hogar',
                'descripcion': 'Artículos para el hogar y decoración'
            },
            {
                'nombre': 'Deportes',
                'descripcion': 'Equipamiento deportivo y fitness'
            },
            {
                'nombre': 'Libros',
                'descripcion': 'Libros físicos y digitales de diversos géneros'
            },
        ]
        
        categorias = {}
        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={'descripcion': cat_data['descripcion']}
            )
            categorias[cat_data['nombre']] = categoria
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Categoría creada: {categoria.nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'○ Categoría ya existe: {categoria.nombre}'))
        
        # Crear productos
        productos_data = [
            {
                'nombre': 'Laptop HP 15"',
                'descripcion': 'Laptop HP de 15 pulgadas con procesador Intel Core i5, 8GB RAM, 256GB SSD',
                'precio': 599.99,
                'stock': 15,
                'categorias': ['Electrónica']
            },
            {
                'nombre': 'Mouse Inalámbrico Logitech',
                'descripcion': 'Mouse inalámbrico ergonómico con sensor de precisión y batería de larga duración',
                'precio': 29.99,
                'stock': 50,
                'categorias': ['Electrónica']
            },
            {
                'nombre': 'Camiseta Polo',
                'descripcion': 'Camiseta tipo polo de algodón 100%, disponible en varios colores',
                'precio': 19.99,
                'stock': 100,
                'categorias': ['Ropa']
            },
            {
                'nombre': 'Jeans Clásicos',
                'descripcion': 'Pantalones jeans de corte clásico, mezclilla de alta calidad',
                'precio': 49.99,
                'stock': 75,
                'categorias': ['Ropa']
            },
            {
                'nombre': 'Lámpara LED de Escritorio',
                'descripcion': 'Lámpara LED ajustable con control de intensidad y temperatura de color',
                'precio': 39.99,
                'stock': 30,
                'categorias': ['Hogar', 'Electrónica']
            },
            {
                'nombre': 'Juego de Sábanas Premium',
                'descripcion': 'Juego de sábanas de algodón egipcio 400 hilos, incluye funda de almohada',
                'precio': 89.99,
                'stock': 25,
                'categorias': ['Hogar']
            },
            {
                'nombre': 'Balón de Fútbol Profesional',
                'descripcion': 'Balón de fútbol reglamentario, cuero sintético de alta calidad',
                'precio': 34.99,
                'stock': 40,
                'categorias': ['Deportes']
            },
            {
                'nombre': 'Mancuernas Ajustables 20kg',
                'descripcion': 'Par de mancuernas con peso ajustable de 5 a 20kg cada una',
                'precio': 79.99,
                'stock': 20,
                'categorias': ['Deportes']
            },
            {
                'nombre': 'Cien Años de Soledad',
                'descripcion': 'Novela de Gabriel García Márquez, edición conmemorativa',
                'precio': 24.99,
                'stock': 60,
                'categorias': ['Libros']
            },
            {
                'nombre': 'Python para Principiantes',
                'descripcion': 'Guía completa de programación en Python con ejemplos prácticos',
                'precio': 34.99,
                'stock': 45,
                'categorias': ['Libros']
            },
            {
                'nombre': 'Smartphone Samsung Galaxy',
                'descripcion': 'Smartphone con pantalla AMOLED 6.5", 128GB almacenamiento, cámara triple',
                'precio': 449.99,
                'stock': 12,
                'categorias': ['Electrónica']
            },
            {
                'nombre': 'Auriculares Bluetooth',
                'descripcion': 'Auriculares inalámbricos con cancelación de ruido y 30 horas de batería',
                'precio': 99.99,
                'stock': 35,
                'categorias': ['Electrónica']
            },
            {
                'nombre': 'Chaqueta Deportiva',
                'descripcion': 'Chaqueta impermeable y transpirable para running y actividades al aire libre',
                'precio': 69.99,
                'stock': 40,
                'categorias': ['Ropa', 'Deportes']
            },
            {
                'nombre': 'Cafetera Espresso',
                'descripcion': 'Cafetera espresso automática con molinillo integrado y sistema de vapor',
                'precio': 299.99,
                'stock': 8,
                'categorias': ['Hogar', 'Electrónica']
            },
            {
                'nombre': 'Esterilla de Yoga',
                'descripcion': 'Esterilla antideslizante de 6mm de grosor con bolsa de transporte',
                'precio': 29.99,
                'stock': 55,
                'categorias': ['Deportes']
            },
        ]
        
        for prod_data in productos_data:
            categorias_nombres = prod_data.pop('categorias')
            producto, created = Producto.objects.get_or_create(
                nombre=prod_data['nombre'],
                defaults=prod_data
            )
            
            if created:
                # Asignar categorías al producto
                for cat_nombre in categorias_nombres:
                    if cat_nombre in categorias:
                        ProductoCategoria.objects.get_or_create(
                            producto=producto,
                            categoria=categorias[cat_nombre]
                        )
                self.stdout.write(self.style.SUCCESS(f'✓ Producto creado: {producto.nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'○ Producto ya existe: {producto.nombre}'))
        
        self.stdout.write(self.style.SUCCESS('\n¡Datos de prueba creados exitosamente!'))
        self.stdout.write(self.style.SUCCESS(f'Total categorías: {Categoria.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total productos: {Producto.objects.count()}'))
