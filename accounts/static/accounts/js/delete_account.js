// Toggle para mostrar/ocultar contraseña
document.getElementById('togglePassword').addEventListener('click', function() {
    const passwordInput = document.getElementById('password');
    const eyeIcon = document.getElementById('eyeIcon');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.classList.remove('bi-eye');
        eyeIcon.classList.add('bi-eye-slash');
    } else {
        passwordInput.type = 'password';
        eyeIcon.classList.remove('bi-eye-slash');
        eyeIcon.classList.add('bi-eye');
    }
});

// Habilitar botones solo cuando se cumplan las condiciones
const passwordInput = document.getElementById('password');
const confirmTextInput = document.getElementById('confirm_text');
const deactivateButton = document.getElementById('deactivateButton');
const deleteButton = document.getElementById('deleteButton');
const actionInput = document.getElementById('actionInput');
const immediateConfirmContainer = document.getElementById('immediateConfirmContainer');
const confirmImmediateCheckbox = document.getElementById('confirm_immediate');

function checkFormValidity() {
    const passwordFilled = passwordInput.value.trim().length > 0;
    const confirmTextCorrect = confirmTextInput.value.trim() === 'ELIMINAR MI CUENTA';
    
    if (passwordFilled && confirmTextCorrect) {
        deactivateButton.disabled = false;
        deleteButton.disabled = false;
    } else {
        deactivateButton.disabled = true;
        deleteButton.disabled = true;
    }
}

passwordInput.addEventListener('input', checkFormValidity);
confirmTextInput.addEventListener('input', checkFormValidity);

// Manejar clic en botón de desactivar
deactivateButton.addEventListener('click', function(e) {
    e.preventDefault();
    actionInput.value = 'deactivate';
    immediateConfirmContainer.style.display = 'none';
    
    const confirmed = confirm(
        '⚠️ CONFIRMACIÓN REQUERIDA ⚠️\n\n' +
        'Tu cuenta será DESACTIVADA inmediatamente y se eliminará en 30 días.\n\n' +
        'Durante este periodo podrás cancelar la eliminación.\n\n' +
        '¿Deseas continuar?'
    );
    
    if (confirmed) {
        document.getElementById('deleteAccountForm').submit();
    }
});

// Manejar clic en botón de eliminar inmediatamente
deleteButton.addEventListener('click', function(e) {
    e.preventDefault();
    actionInput.value = 'delete_now';
    immediateConfirmContainer.style.display = 'block';
    
    // Esperar a que se marque el checkbox
    setTimeout(function() {
        if (!confirmImmediateCheckbox.checked) {
            alert('⚠️ Para eliminar inmediatamente debes marcar la casilla de confirmación.');
            return;
        }
        
        const confirmed = confirm(
            '🚨 ÚLTIMA ADVERTENCIA - ELIMINACIÓN INMEDIATA 🚨\n\n' +
            'Tu cuenta será eliminada AHORA MISMO y PERMANENTEMENTE.\n\n' +
            'NO PODRÁS recuperarla ni sus datos.\n\n' +
            '¿Estás COMPLETAMENTE seguro?'
        );
        
        if (confirmed) {
            document.getElementById('deleteAccountForm').submit();
        }
    }, 100);
});
