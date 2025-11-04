// Función para mostrar/ocultar contraseña
function togglePasswordVisibility(inputId, buttonId) {
    const input = document.getElementById(inputId);
    const button = document.getElementById(buttonId);
    const icon = button.querySelector('i');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Validación en tiempo real de la contraseña
document.addEventListener('DOMContentLoaded', function() {
    const password1 = document.getElementById('password1');
    const password2 = document.getElementById('password2');
    
    function validatePassword() {
        const pwd = password1.value;
        const pwd2 = password2.value;
        
        // Longitud
        const lengthReq = document.getElementById('req-length');
        if (pwd.length >= 8 && pwd.length <= 20) {
            lengthReq.classList.add('requirement-met');
            lengthReq.classList.remove('requirement-failed');
        } else if (pwd.length > 0) {
            lengthReq.classList.add('requirement-failed');
            lengthReq.classList.remove('requirement-met');
        } else {
            lengthReq.classList.remove('requirement-met', 'requirement-failed');
        }
        
        // Mayúscula
        const uppercaseReq = document.getElementById('req-uppercase');
        if (/[A-Z]/.test(pwd)) {
            uppercaseReq.classList.add('requirement-met');
            uppercaseReq.classList.remove('requirement-failed');
        } else if (pwd.length > 0) {
            uppercaseReq.classList.add('requirement-failed');
            uppercaseReq.classList.remove('requirement-met');
        } else {
            uppercaseReq.classList.remove('requirement-met', 'requirement-failed');
        }
        
        // Minúscula
        const lowercaseReq = document.getElementById('req-lowercase');
        if (/[a-z]/.test(pwd)) {
            lowercaseReq.classList.add('requirement-met');
            lowercaseReq.classList.remove('requirement-failed');
        } else if (pwd.length > 0) {
            lowercaseReq.classList.add('requirement-failed');
            lowercaseReq.classList.remove('requirement-met');
        } else {
            lowercaseReq.classList.remove('requirement-met', 'requirement-failed');
        }
        
        // Carácter especial
        const specialReq = document.getElementById('req-special');
        if (/[!¡@#$%^&*.\-_+(){}\[\]:;<>?,/\\|~`]/.test(pwd)) {
            specialReq.classList.add('requirement-met');
            specialReq.classList.remove('requirement-failed');
        } else if (pwd.length > 0) {
            specialReq.classList.add('requirement-failed');
            specialReq.classList.remove('requirement-met');
        } else {
            specialReq.classList.remove('requirement-met', 'requirement-failed');
        }
        
        // Sin espacios
        const spacesReq = document.getElementById('req-no-spaces');
        const emojiRegex = /[\u{1F300}-\u{1F9FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]/u;
        if (!/\s/.test(pwd) && !emojiRegex.test(pwd) && pwd.length > 0) {
            spacesReq.classList.add('requirement-met');
            spacesReq.classList.remove('requirement-failed');
        } else if (pwd.length > 0) {
            spacesReq.classList.add('requirement-failed');
            spacesReq.classList.remove('requirement-met');
        } else {
            spacesReq.classList.remove('requirement-met', 'requirement-failed');
        }
        
        // Sin caracteres consecutivos (1.8)
        const consecutiveReq = document.getElementById('req-no-consecutive');
        function hasConsecutiveChars(str) {
            // Verificar 3 o más caracteres idénticos consecutivos (aaa, 111)
            if (/(.)\1{2,}/.test(str)) return true;
            
            // Verificar secuencias alfabéticas (abc, xyz)
            for (let i = 0; i < str.length - 2; i++) {
                const charCode1 = str.charCodeAt(i);
                const charCode2 = str.charCodeAt(i + 1);
                const charCode3 = str.charCodeAt(i + 2);
                
                if (charCode2 === charCode1 + 1 && charCode3 === charCode2 + 1) {
                    return true;
                }
            }
            
            // Verificar secuencias numéricas (123, 789)
            for (let i = 0; i < str.length - 2; i++) {
                if (/\d/.test(str[i]) && /\d/.test(str[i+1]) && /\d/.test(str[i+2])) {
                    const num1 = parseInt(str[i]);
                    const num2 = parseInt(str[i+1]);
                    const num3 = parseInt(str[i+2]);
                    
                    if (num2 === num1 + 1 && num3 === num2 + 1) {
                        return true;
                    }
                }
            }
            
            return false;
        }
        
        if (!hasConsecutiveChars(pwd) && pwd.length > 0) {
            consecutiveReq.classList.add('requirement-met');
            consecutiveReq.classList.remove('requirement-failed');
        } else if (pwd.length > 0) {
            consecutiveReq.classList.add('requirement-failed');
            consecutiveReq.classList.remove('requirement-met');
        } else {
            consecutiveReq.classList.remove('requirement-met', 'requirement-failed');
        }
        
        // Contraseñas coinciden
        const matchReq = document.getElementById('req-match');
        if (pwd2.length > 0) {
            if (pwd === pwd2 && pwd.length > 0) {
                matchReq.classList.add('requirement-met');
                matchReq.classList.remove('requirement-failed');
            } else {
                matchReq.classList.add('requirement-failed');
                matchReq.classList.remove('requirement-met');
            }
        } else {
            matchReq.classList.remove('requirement-met', 'requirement-failed');
        }
    }
    
    password1.addEventListener('input', validatePassword);
    password2.addEventListener('input', validatePassword);
});
