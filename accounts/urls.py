"""
URLs para la aplicación de autenticación y usuarios
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Verificación de email
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    
    # Restablecimiento de contraseña
    path('reset-password/', views.password_reset_request, name='password_reset_request'),
    path('reset-password/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    
    # Dashboards
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    
    # Perfil
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('active-sessions/', views.active_sessions_view, name='active_sessions'),
    path('close-session/<int:session_id>/', views.close_session_view, name='close_session'),
    path('close-all-sessions/', views.close_all_sessions_view, name='close_all_sessions'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
    path('cancel-deletion/', views.cancel_account_deletion, name='cancel_deletion'),
    path('export-data/', views.export_user_data, name='export_data'),
    
    # Gestión de usuarios (Admin)
    path('users/', views.user_list_view, name='user_list'),
    path('admin/user/<int:user_id>/view/', views.user_view_ajax, name='user_view_ajax'),
    path('admin/user/<int:user_id>/edit/', views.user_edit_ajax, name='user_edit_ajax'),
    path('admin/user/<int:user_id>/delete/', views.user_delete_ajax, name='user_delete_ajax'),
]
