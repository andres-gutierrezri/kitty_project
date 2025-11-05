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
deactivateButton.addEventListener('click', async function(e) {
    e.preventDefault();
    actionInput.value = 'deactivate';
    immediateConfirmContainer.style.display = 'none';
    
    const confirmed = await showConfirm(
        'Tu cuenta será <strong>DESACTIVADA</strong> inmediatamente y se eliminará en <strong>30 días</strong>.<br><br>' +
        'Durante este periodo podrás <span class="text-success">cancelar la eliminación</span> iniciando sesión.<br><br>' +
        '¿Deseas continuar?',
        {
            title: '⚠️ Confirmación Requerida',
            confirmText: 'Sí, desactivar mi cuenta',
            cancelText: 'No, cancelar'
        }
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
    setTimeout(async function() {
        if (!confirmImmediateCheckbox.checked) {
            await showWarning(
                'Para eliminar inmediatamente tu cuenta debes marcar la casilla de confirmación.',
                { title: '⚠️ Confirmación Requerida' }
            );
            actionInput.value = '';
            immediateConfirmContainer.style.display = 'none';
            return;
        }
        
        const confirmed = await showConfirm(
            '🚨 <strong>ÚLTIMA ADVERTENCIA - ELIMINACIÓN INMEDIATA</strong> 🚨<br><br>' +
            'Tu cuenta será eliminada <strong>AHORA MISMO</strong> y <strong>PERMANENTEMENTE</strong>.<br><br>' +
            '<span class="text-danger fw-bold">NO PODRÁS</span> recuperarla ni sus datos.<br><br>' +
            '¿Estás <strong>COMPLETAMENTE</strong> seguro?',
            {
                title: '🚨 Última Advertencia',
                confirmText: 'Sí, eliminar permanentemente',
                cancelText: 'No, cancelar'
            }
        );
        
        if (confirmed) {
            document.getElementById('deleteAccountForm').submit();
        } else {
            actionInput.value = '';
            immediateConfirmContainer.style.display = 'none';
            confirmImmediateCheckbox.checked = false;
        }
    }, 100);
});
