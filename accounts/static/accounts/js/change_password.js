// Toggle mostrar/ocultar contraseña
document.querySelectorAll('.toggle-password').forEach(icon => {
    icon.addEventListener('click', function() {
        const targetId = this.getAttribute('data-target');
        const passwordInput = document.getElementById(targetId);
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            this.classList.remove('fa-eye');
            this.classList.add('fa-eye-slash');
        } else {
            passwordInput.type = 'password';
            this.classList.remove('fa-eye-slash');
            this.classList.add('fa-eye');
        }
    });
});

// Confirmación antes de enviar
document.getElementById('changePasswordForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const confirmed = await showConfirm(
        '¿Estás seguro de que deseas cambiar tu contraseña?<br><br>' +
        'Tu sesión se cerrará y tendrás que <strong>iniciar sesión nuevamente</strong> con tu nueva contraseña.',
        {
            title: '🔐 Cambiar Contraseña',
            confirmText: 'Sí, cambiar contraseña',
            cancelText: 'No, cancelar'
        }
    );
    
    if (confirmed) {
        e.target.submit();
    }
});

// Validación en tiempo real
const newPassword = document.getElementById('new-password');
const confirmPassword = document.getElementById('confirm-password');

function validatePasswords() {
    if (newPassword.value && confirmPassword.value) {
        if (newPassword.value !== confirmPassword.value) {
            confirmPassword.setCustomValidity('Las contraseñas no coinciden');
        } else {
            confirmPassword.setCustomValidity('');
        }
    }
}

newPassword.addEventListener('input', validatePasswords);
confirmPassword.addEventListener('input', validatePasswords);
