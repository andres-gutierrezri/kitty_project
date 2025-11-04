/**
 * ========================================
 * JAVASCRIPT DE AUTENTICACIÓN
 * Archivo: auth.js
 * ========================================
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // Toggle Password Visibility
    // ==========================================
    const togglePasswordButtons = document.querySelectorAll('.password-toggle');
    
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            let passwordInput;
            
            if (targetId) {
                passwordInput = document.getElementById(targetId);
            } else {
                passwordInput = this.parentElement.querySelector('input[type="password"], input[type="text"]');
            }
            
            if (passwordInput) {
                const icon = this.querySelector('i');
                
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                } else {
                    passwordInput.type = 'password';
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }
            }
        });
    });
    
    // ==========================================
    // Form Validation
    // ==========================================
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = document.getElementById('login-username').value.trim();
            const password = document.getElementById('login-password').value;
            
            if (!username || !password) {
                e.preventDefault();
                showAlert('Por favor, completa todos los campos', 'danger');
                return false;
            }
        });
    }
    
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const password1 = document.getElementById('register-password1').value;
            const password2 = document.getElementById('register-password2').value;
            const termsCheck = document.getElementById('terms-check');
            
            if (password1 !== password2) {
                e.preventDefault();
                showAlert('Las contraseñas no coinciden', 'danger');
                return false;
            }
            
            if (!termsCheck.checked) {
                e.preventDefault();
                showAlert('Debes aceptar los términos y condiciones', 'warning');
                return false;
            }
        });
    }
    
    // ==========================================
    // Auto-dismiss Alerts
    // ==========================================
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
});

/**
 * Muestra un mensaje de alerta
 * @param {string} message - Mensaje a mostrar
 * @param {string} type - Tipo de alerta (success, danger, warning, info)
 */
function showAlert(message, type = 'info') {
    const messagesContainer = document.querySelector('.messages-container');
    
    if (messagesContainer) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        messagesContainer.appendChild(alertDiv);
        
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
}
