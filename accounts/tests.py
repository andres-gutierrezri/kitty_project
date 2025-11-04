"""
Tests para la aplicación de autenticación y usuarios
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserRole, LoginHistory

User = get_user_model()


class UserRoleModelTest(TestCase):
    """Tests para el modelo UserRole"""
    
    def setUp(self):
        self.role = UserRole.objects.create(
            name='ADMIN',
            description='Administrador del sistema'
        )
    
    def test_role_creation(self):
        """Test de creación de rol"""
        self.assertEqual(self.role.name, 'ADMIN')
        self.assertEqual(str(self.role), 'Administrador')
    
    def test_role_unique(self):
        """Test de unicidad de rol"""
        with self.assertRaises(Exception):
            UserRole.objects.create(name='ADMIN')


class CustomUserModelTest(TestCase):
    """Tests para el modelo CustomUser"""
    
    def setUp(self):
        self.role = UserRole.objects.create(
            name='USER',
            description='Usuario estándar'
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role=self.role
        )
    
    def test_user_creation(self):
        """Test de creación de usuario"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
    
    def test_user_role_display(self):
        """Test del método get_role_display"""
        self.assertEqual(self.user.get_role_display(), 'Usuario')
    
    def test_user_is_admin(self):
        """Test del método is_admin"""
        self.assertFalse(self.user.is_admin())
        
        admin_role = UserRole.objects.create(name='ADMIN')
        self.user.role = admin_role
        self.user.save()
        self.assertTrue(self.user.is_admin())


class AuthViewsTest(TestCase):
    """Tests para las vistas de autenticación"""
    
    def setUp(self):
        self.role = UserRole.objects.create(name='USER')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=self.role
        )
    
    def test_login_page_loads(self):
        """Test de carga de página de login"""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_register_page_loads(self):
        """Test de carga de página de registro"""
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
    
    def test_login_success(self):
        """Test de inicio de sesión exitoso"""
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)  # Redirección
    
    def test_dashboard_requires_login(self):
        """Test de que el dashboard requiere login"""
        response = self.client.get('/accounts/dashboard/')
        self.assertEqual(response.status_code, 302)  # Redirección a login
