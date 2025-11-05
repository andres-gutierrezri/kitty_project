/**
 * ========================================
 * JAVASCRIPT DE LISTA DE USUARIOS
 * Archivo: user-list.js
 * ========================================
 */

document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    // ==========================================
    // DataTables Initialization
    // ==========================================
    let usersTable;
    if (typeof jQuery !== 'undefined' && jQuery.fn.DataTable) {
        usersTable = $('#users-table').DataTable({
            language: {
                url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json'
            },
            order: [[0, 'desc']],
            pageLength: 25,
            responsive: true
        });
    }
    
    // ==========================================
    // MODAL VER USUARIO
    // ==========================================
    
    const viewUserModal = new bootstrap.Modal(document.getElementById('viewUserModal'));
    const viewUserContent = document.getElementById('viewUserContent');
    
    // Botones Ver Usuario
    document.querySelectorAll('.btn-view-user').forEach(button => {
        button.addEventListener('click', async function() {
            const userId = this.getAttribute('data-user-id');
            
            // Mostrar loading
            viewUserContent.innerHTML = `
                <div class="text-center">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Cargando...</span>
                    </div>
                    <p class="mt-2">Cargando información del usuario...</p>
                </div>
            `;
            
            // Mostrar modal
            viewUserModal.show();
            
            try {
                const response = await fetch(`/accounts/admin/user/${userId}/view/`);
                
                if (!response.ok) {
                    throw new Error('Error al cargar los datos');
                }
                
                const data = await response.json();
                
                // Renderizar datos del usuario
                viewUserContent.innerHTML = `
                    <div class="row">
                        <div class="col-md-6">
                            <h6 class="text-primary border-bottom pb-2">
                                <i class="fas fa-user"></i> Información Personal
                            </h6>
                            <table class="table table-sm">
                                <tr>
                                    <th width="40%">ID:</th>
                                    <td>${data.id}</td>
                                </tr>
                                <tr>
                                    <th>Usuario:</th>
                                    <td><strong>@${data.username}</strong></td>
                                </tr>
                                <tr>
                                    <th>Nombre:</th>
                                    <td>${data.first_name || '-'}</td>
                                </tr>
                                <tr>
                                    <th>Apellido:</th>
                                    <td>${data.last_name || '-'}</td>
                                </tr>
                                <tr>
                                    <th>Email:</th>
                                    <td>${data.email}</td>
                                </tr>
                                <tr>
                                    <th>Teléfono:</th>
                                    <td>${data.phone_number || '-'}</td>
                                </tr>
                            </table>
                        </div>
                        <div class="col-md-6">
                            <h6 class="text-success border-bottom pb-2">
                                <i class="fas fa-shield-alt"></i> Información del Sistema
                            </h6>
                            <table class="table table-sm">
                                <tr>
                                    <th width="50%">Rol:</th>
                                    <td><span class="badge bg-primary">${data.role_display}</span></td>
                                </tr>
                                <tr>
                                    <th>Estado:</th>
                                    <td>
                                        ${data.is_active 
                                            ? '<span class="badge bg-success">Activo</span>' 
                                            : '<span class="badge bg-secondary">Inactivo</span>'}
                                    </td>
                                </tr>
                                <tr>
                                    <th>Superusuario:</th>
                                    <td>
                                        ${data.is_superuser 
                                            ? '<span class="badge bg-danger">Sí</span>' 
                                            : '<span class="badge bg-secondary">No</span>'}
                                    </td>
                                </tr>
                                <tr>
                                    <th>Email Verificado:</th>
                                    <td>
                                        ${data.email_verified 
                                            ? '<span class="badge bg-success">Verificado</span>' 
                                            : '<span class="badge bg-warning">No verificado</span>'}
                                    </td>
                                </tr>
                                <tr>
                                    <th>Registro:</th>
                                    <td>${data.date_joined}</td>
                                </tr>
                                <tr>
                                    <th>Último acceso:</th>
                                    <td>${data.last_login || 'Nunca'}</td>
                                </tr>
                            </table>
                        </div>
                    </div>
                    
                    ${data.bio ? `
                        <div class="mt-3">
                            <h6 class="text-info border-bottom pb-2">
                                <i class="fas fa-info-circle"></i> Biografía
                            </h6>
                            <p class="text-muted">${data.bio}</p>
                        </div>
                    ` : ''}
                    
                    <div class="mt-3">
                        <h6 class="text-warning border-bottom pb-2">
                            <i class="fas fa-chart-bar"></i> Estadísticas
                        </h6>
                        <div class="row text-center">
                            <div class="col-4">
                                <div class="p-3 bg-light rounded">
                                    <h4 class="mb-0 text-primary">${data.reviews_count || 0}</h4>
                                    <small class="text-muted">Reseñas</small>
                                </div>
                            </div>
                            <div class="col-4">
                                <div class="p-3 bg-light rounded">
                                    <h4 class="mb-0 text-success">${data.favorites_count || 0}</h4>
                                    <small class="text-muted">Favoritos</small>
                                </div>
                            </div>
                            <div class="col-4">
                                <div class="p-3 bg-light rounded">
                                    <h4 class="mb-0 text-info">${data.sessions_count || 0}</h4>
                                    <small class="text-muted">Sesiones</small>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                
            } catch (error) {
                console.error('Error:', error);
                viewUserContent.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle"></i>
                        Error al cargar la información del usuario.
                    </div>
                `;
            }
        });
    });
    
    // ==========================================
    // MODAL EDITAR USUARIO
    // ==========================================
    
    const editUserModal = new bootstrap.Modal(document.getElementById('editUserModal'));
    const editUserContent = document.getElementById('editUserContent');
    const editUserForm = document.getElementById('editUserForm');
    let currentEditUserId = null;
    
    // Botones Editar Usuario
    document.querySelectorAll('.btn-edit-user').forEach(button => {
        button.addEventListener('click', async function() {
            const userId = this.getAttribute('data-user-id');
            currentEditUserId = userId;
            
            // Mostrar loading
            editUserContent.innerHTML = `
                <div class="text-center">
                    <div class="spinner-border text-warning" role="status">
                        <span class="visually-hidden">Cargando...</span>
                    </div>
                    <p class="mt-2">Cargando formulario...</p>
                </div>
            `;
            
            // Mostrar modal
            editUserModal.show();
            
            try {
                const response = await fetch(`/accounts/admin/user/${userId}/edit/`);
                
                if (!response.ok) {
                    throw new Error('Error al cargar el formulario');
                }
                
                const data = await response.json();
                
                // Renderizar formulario
                editUserContent.innerHTML = `
                    <input type="hidden" name="user_id" value="${userId}">
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">
                                <i class="fas fa-user"></i> Nombre de Usuario *
                            </label>
                            <input type="text" class="form-control" name="username" 
                                   value="${data.username}" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">
                                <i class="fas fa-envelope"></i> Email *
                            </label>
                            <input type="email" class="form-control" name="email" 
                                   value="${data.email}" required>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">
                                <i class="fas fa-signature"></i> Nombre
                            </label>
                            <input type="text" class="form-control" name="first_name" 
                                   value="${data.first_name || ''}">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">
                                <i class="fas fa-signature"></i> Apellido
                            </label>
                            <input type="text" class="form-control" name="last_name" 
                                   value="${data.last_name || ''}">
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">
                                <i class="fas fa-phone"></i> Teléfono
                            </label>
                            <input type="text" class="form-control" name="phone_number" 
                                   value="${data.phone_number || ''}">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">
                                <i class="fas fa-user-tag"></i> Rol
                            </label>
                            <select class="form-select" name="role_id">
                                ${data.roles.map(role => `
                                    <option value="${role.id}" ${role.id === data.role_id ? 'selected' : ''}>
                                        ${role.name}
                                    </option>
                                `).join('')}
                            </select>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" name="is_active" 
                                       id="edit_is_active" ${data.is_active ? 'checked' : ''}>
                                <label class="form-check-label" for="edit_is_active">
                                    <i class="fas fa-check-circle"></i> Cuenta Activa
                                </label>
                            </div>
                        </div>
                        <div class="col-md-6 mb-3">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" name="email_verified" 
                                       id="edit_email_verified" ${data.email_verified ? 'checked' : ''}>
                                <label class="form-check-label" for="edit_email_verified">
                                    <i class="fas fa-envelope-check"></i> Email Verificado
                                </label>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">
                            <i class="fas fa-align-left"></i> Biografía
                        </label>
                        <textarea class="form-control" name="bio" rows="3">${data.bio || ''}</textarea>
                    </div>
                    
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle"></i>
                        Los campos marcados con * son obligatorios
                    </div>
                `;
                
            } catch (error) {
                console.error('Error:', error);
                editUserContent.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle"></i>
                        Error al cargar el formulario de edición.
                    </div>
                `;
            }
        });
    });
    
    // Submit del formulario de edición
    editUserForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const submitButton = this.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        
        // Deshabilitar botón
        submitButton.disabled = true;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';
        
        try {
            const response = await fetch(`/accounts/admin/user/${currentEditUserId}/edit/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                await showSuccess('Usuario actualizado correctamente');
                editUserModal.hide();
                location.reload();
            } else {
                await showError(data.message || 'Error al actualizar el usuario');
                submitButton.disabled = false;
                submitButton.innerHTML = originalText;
            }
            
        } catch (error) {
            console.error('Error:', error);
            await showError('Error al procesar la solicitud');
            submitButton.disabled = false;
            submitButton.innerHTML = originalText;
        }
    });
    
    // ==========================================
    // MODAL ELIMINAR USUARIO
    // ==========================================
    
    const deleteUserModal = new bootstrap.Modal(document.getElementById('deleteUserModal'));
    const confirmDeleteCheckbox = document.getElementById('confirmDeleteCheckbox');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    const deleteUserName = document.getElementById('deleteUserName');
    let currentDeleteUserId = null;
    
    // Botones Eliminar Usuario
    document.querySelectorAll('.btn-delete-user').forEach(button => {
        button.addEventListener('click', function() {
            currentDeleteUserId = this.getAttribute('data-user-id');
            const username = this.getAttribute('data-user-name');
            
            // Actualizar nombre en el modal
            deleteUserName.textContent = '@' + username;
            
            // Resetear checkbox
            confirmDeleteCheckbox.checked = false;
            confirmDeleteBtn.disabled = true;
            
            // Mostrar modal
            deleteUserModal.show();
        });
    });
    
    // Habilitar botón cuando se marca el checkbox
    confirmDeleteCheckbox.addEventListener('change', function() {
        confirmDeleteBtn.disabled = !this.checked;
    });
    
    // Confirmar eliminación
    confirmDeleteBtn.addEventListener('click', async function() {
        if (!currentDeleteUserId || !confirmDeleteCheckbox.checked) {
            return;
        }
        
        const originalText = this.innerHTML;
        this.disabled = true;
        this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Eliminando...';
        
        try {
            const response = await fetch(`/accounts/admin/user/${currentDeleteUserId}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                await showSuccess('Usuario eliminado correctamente');
                deleteUserModal.hide();
                location.reload();
            } else {
                await showError(data.message || 'Error al eliminar el usuario');
                this.disabled = false;
                this.innerHTML = originalText;
            }
            
        } catch (error) {
            console.error('Error:', error);
            await showError('Error al procesar la solicitud');
            this.disabled = false;
            this.innerHTML = originalText;
        }
    });
    
    console.log('✅ Sistema de gestión de usuarios cargado correctamente');
    
});
