/**
 * ========================================
 * JAVASCRIPT DE REGISTRO
 * Archivo: register.js
 * ========================================
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // Password Strength Indicator
    // ==========================================
    const password1Input = document.getElementById('register-password1');
    
    if (password1Input) {
        password1Input.addEventListener('input', function() {
            checkPasswordStrength(this.value);
        });
    }
    
    // ==========================================
    // Username Availability Check
    // ==========================================
    const usernameInput = document.getElementById('register-username');
    
    if (usernameInput) {
        usernameInput.addEventListener('blur', function() {
            const username = this.value.trim();
            if (username.length >= 3) {
                // Aquí podrías hacer una petición AJAX para verificar disponibilidad
                console.log('Verificando disponibilidad de username:', username);
            }
        });
    }
    
});

/**
 * Verifica la fortaleza de la contraseña
 * @param {string} password - Contraseña a verificar
 */
function checkPasswordStrength(password) {
    let strength = 0;
    let message = '';
    let color = '';
    
    // Criterios de fortaleza
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]/)) strength++;
    if (password.match(/[A-Z]/)) strength++;
    if (password.match(/[0-9]/)) strength++;
    if (password.match(/[^a-zA-Z0-9]/)) strength++;
    
    // Determinar nivel y mensaje
    switch(strength) {
        case 0:
        case 1:
            message = 'Muy débil';
            color = 'danger';
            break;
        case 2:
            message = 'Débil';
            color = 'warning';
            break;
        case 3:
            message = 'Media';
            color = 'info';
            break;
        case 4:
            message = 'Fuerte';
            color = 'success';
            break;
        case 5:
            message = 'Muy fuerte';
            color = 'success';
            break;
    }
    
    // Mostrar indicador (si existe un elemento para ello)
    const strengthIndicator = document.getElementById('password-strength');
    if (strengthIndicator) {
        strengthIndicator.innerHTML = `
            <div class="progress mt-2">
                <div class="progress-bar bg-${color}" role="progressbar" 
                     style="width: ${(strength/5)*100}%" 
                     aria-valuenow="${strength}" aria-valuemin="0" aria-valuemax="5">
                    ${message}
                </div>
            </div>
        `;
    }
}
