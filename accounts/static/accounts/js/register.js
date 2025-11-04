/**
 * ========================================
 * JAVASCRIPT DE REGISTRO OPTIMIZADO
 * Archivo: register.js
 * Versión: 2.0 - Optimizado para producción
 * ========================================
 */

(function() {
    'use strict';

    // ==========================================
    // CONFIGURACIÓN Y CONSTANTES
    // ==========================================
    const DEBOUNCE_DELAY = 300; // ms - reducido para mejor UX
    const MIN_USERNAME_LENGTH = 3;
    const MIN_PASSWORD_LENGTH = 8;
    const MAX_PASSWORD_LENGTH = 20;

    // Expresiones regulares compiladas (mejor rendimiento)
    const REGEX = {
        uppercase: /[A-Z]/,
        lowercase: /[a-z]/,
        special: /[!@#$%^&*.\-_+(){}[\]:;<>?,/\\|~`]/,
        spaces: /\s/,
        email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        consecutive: {
            identical: /(.)\1{2,}/,
            alphabetic: /(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)/i,
            numeric: /(?:012|123|234|345|456|567|678|789)/
        }
    };

    // Cache de elementos DOM
    const elements = {};

    // ==========================================
    // UTILIDADES
    // ==========================================

    /**
     * Función de debounce optimizada
     * @param {Function} func - Función a ejecutar
     * @param {number} wait - Tiempo de espera en ms
     * @returns {Function} Función con debounce
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Actualiza el ícono de validación de un requisito
     * @param {HTMLElement} element - Elemento del requisito
     * @param {boolean} isValid - Si cumple el requisito
     */
    function updateRequirementIcon(element, isValid) {
        if (!element) return;
        
        const icon = element.querySelector('.fa-check-circle');
        if (icon) {
            icon.classList.toggle('text-success', isValid);
            icon.classList.toggle('text-muted', !isValid);
        }
    }

    /**
     * Muestra feedback visual en un campo
     * @param {HTMLElement} input - Campo de entrada
     * @param {boolean} isValid - Si es válido
     * @param {string} message - Mensaje de error (opcional)
     */
    function showFieldFeedback(input, isValid, message = '') {
        if (!input) return;

        input.classList.toggle('is-valid', isValid);
        input.classList.toggle('is-invalid', !isValid);

        // Actualizar o crear mensaje de feedback
        let feedbackElement = input.parentElement.querySelector('.invalid-feedback');
        if (!isValid && message && feedbackElement) {
            feedbackElement.textContent = message;
            feedbackElement.style.display = 'block';
        } else if (feedbackElement) {
            feedbackElement.style.display = 'none';
        }
    }

    // ==========================================
    // VALIDADORES DE CONTRASEÑA
    // ==========================================

    /**
     * Valida todos los requisitos de la contraseña
     * @param {string} password - Contraseña a validar
     * @param {Object} userData - Datos del usuario para comparación
     * @returns {Object} Objeto con resultados de validación
     */
    function validatePasswordRequirements(password, userData = {}) {
        const results = {
            length: password.length >= MIN_PASSWORD_LENGTH && password.length <= MAX_PASSWORD_LENGTH,
            uppercase: REGEX.uppercase.test(password),
            lowercase: REGEX.lowercase.test(password),
            special: REGEX.special.test(password),
            noSpaces: !REGEX.spaces.test(password) && !/[\u{1F300}-\u{1F9FF}]/u.test(password),
            notSimilar: true,
            noConsecutive: true
        };

        // Validar similitud con datos del usuario
        if (password.length >= 3) {
            const passwordLower = password.toLowerCase();
            const { username = '', firstName = '', lastName = '', email = '' } = userData;
            
            const userDataArray = [username, firstName, lastName, email.split('@')[0]]
                .filter(Boolean)
                .map(str => str.toLowerCase());

            results.notSimilar = !userDataArray.some(data => 
                data.length >= 3 && (
                    passwordLower.includes(data) || 
                    data.includes(passwordLower)
                )
            );
        }

        // Validar caracteres consecutivos
        results.noConsecutive = !(
            REGEX.consecutive.identical.test(password) ||
            REGEX.consecutive.alphabetic.test(password) ||
            REGEX.consecutive.numeric.test(password)
        );

        // Calcular si es válida en general
        results.isValid = Object.values(results).every(Boolean);
        
        return results;
    }

    /**
     * Actualiza visualmente los requisitos de contraseña
     * @param {Object} results - Resultados de validación
     */
    function updatePasswordRequirementsUI(results) {
        const requirementsList = document.querySelector('.password-requirements ul');
        if (!requirementsList) return;

        const requirements = requirementsList.querySelectorAll('li');
        const validationOrder = ['length', 'uppercase', 'lowercase', 'special', 'noSpaces', 'notSimilar', 'noConsecutive'];

        requirements.forEach((req, index) => {
            if (validationOrder[index]) {
                updateRequirementIcon(req, results[validationOrder[index]]);
            }
        });
    }

    /**
     * Valida que las contraseñas coincidan
     */
    function validatePasswordMatch() {
        const password1 = elements.password1?.value || '';
        const password2 = elements.password2?.value || '';

        if (password2.length === 0) return;

        const match = password1 === password2;
        showFieldFeedback(
            elements.password2, 
            match, 
            match ? '' : 'Las contraseñas no coinciden'
        );
    }

    // ==========================================
    // VALIDADORES DE CAMPOS
    // ==========================================

    /**
     * Valida el formato del email
     * @param {string} email - Email a validar
     * @returns {boolean} Si el email es válido
     */
    function validateEmail(email) {
        return REGEX.email.test(email);
    }

    /**
     * Valida un campo requerido
     * @param {HTMLElement} input - Campo a validar
     * @param {number} minLength - Longitud mínima
     * @returns {boolean} Si el campo es válido
     */
    function validateRequiredField(input, minLength = 1) {
        if (!input) return false;
        
        const value = input.value.trim();
        const isValid = value.length >= minLength;
        
        showFieldFeedback(
            input, 
            isValid, 
            isValid ? '' : `Este campo debe tener al menos ${minLength} caracteres`
        );
        
        return isValid;
    }

    // ==========================================
    // HANDLERS DE EVENTOS
    // ==========================================

    /**
     * Handler para validación de contraseña (con debounce)
     */
    const handlePasswordInput = debounce(function() {
        const password = elements.password1?.value || '';
        
        if (password.length === 0) {
            // Resetear UI si está vacío
            const requirementsList = document.querySelector('.password-requirements ul');
            if (requirementsList) {
                requirementsList.querySelectorAll('li').forEach(req => {
                    updateRequirementIcon(req, false);
                });
            }
            elements.password1.classList.remove('is-valid', 'is-invalid');
            return;
        }

        // Obtener datos del usuario para validación de similitud
        const userData = {
            username: elements.username?.value || '',
            firstName: elements.firstName?.value || '',
            lastName: elements.lastName?.value || '',
            email: elements.email?.value || ''
        };

        // Validar requisitos
        const results = validatePasswordRequirements(password, userData);
        
        // Actualizar UI
        updatePasswordRequirementsUI(results);
        showFieldFeedback(elements.password1, results.isValid);

        // Validar coincidencia si password2 tiene valor
        if (elements.password2?.value) {
            validatePasswordMatch();
        }
    }, DEBOUNCE_DELAY);

    /**
     * Handler para validación de coincidencia de contraseñas (con debounce)
     */
    const handlePassword2Input = debounce(function() {
        validatePasswordMatch();
    }, DEBOUNCE_DELAY);

    /**
     * Handler para validación de email (con debounce)
     */
    const handleEmailInput = debounce(function() {
        const email = elements.email?.value.trim() || '';
        
        if (email.length === 0) {
            elements.email.classList.remove('is-valid', 'is-invalid');
            return;
        }

        const isValid = validateEmail(email);
        showFieldFeedback(
            elements.email, 
            isValid, 
            isValid ? '' : 'Por favor, ingresa un email válido'
        );
    }, DEBOUNCE_DELAY);

    /**
     * Handler para validación de campos requeridos (con debounce)
     */
    const handleRequiredFieldInput = debounce(function(event) {
        const input = event.target;
        const minLength = input.id.includes('username') ? MIN_USERNAME_LENGTH : 2;
        validateRequiredField(input, minLength);
    }, DEBOUNCE_DELAY);

    /**
     * Handler para envío del formulario
     */
    function handleFormSubmit(event) {
        let isValid = true;

        // Validar todos los campos requeridos
        const requiredFields = [
            { element: elements.firstName, minLength: 2 },
            { element: elements.lastName, minLength: 2 },
            { element: elements.username, minLength: MIN_USERNAME_LENGTH },
            { element: elements.email, minLength: 1 }
        ];

        requiredFields.forEach(({ element, minLength }) => {
            if (element && !validateRequiredField(element, minLength)) {
                isValid = false;
            }
        });

        // Validar email
        if (elements.email?.value && !validateEmail(elements.email.value)) {
            showFieldFeedback(elements.email, false, 'Email inválido');
            isValid = false;
        }

        // Validar contraseñas
        const password = elements.password1?.value || '';
        const userData = {
            username: elements.username?.value || '',
            firstName: elements.firstName?.value || '',
            lastName: elements.lastName?.value || '',
            email: elements.email?.value || ''
        };

        const passwordResults = validatePasswordRequirements(password, userData);
        if (!passwordResults.isValid) {
            showFieldFeedback(elements.password1, false, 'La contraseña no cumple todos los requisitos');
            isValid = false;
        }

        // Validar coincidencia de contraseñas
        if (password !== (elements.password2?.value || '')) {
            showFieldFeedback(elements.password2, false, 'Las contraseñas no coinciden');
            isValid = false;
        }

        // Validar términos y condiciones
        const termsCheck = document.getElementById('terms-check');
        if (termsCheck && !termsCheck.checked) {
            alert('Debes aceptar los términos y condiciones');
            isValid = false;
        }

        if (!isValid) {
            event.preventDefault();
            // Scroll al primer campo con error
            const firstInvalid = document.querySelector('.is-invalid');
            if (firstInvalid) {
                firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstInvalid.focus();
            }
        }
    }

    // ==========================================
    // INICIALIZACIÓN
    // ==========================================

    /**
     * Inicializa el módulo de registro
     */
    function init() {
        // Cachear elementos DOM
        elements.form = document.getElementById('register-form');
        elements.firstName = document.getElementById('register-first-name');
        elements.lastName = document.getElementById('register-last-name');
        elements.username = document.getElementById('register-username');
        elements.email = document.getElementById('register-email');
        elements.password1 = document.getElementById('register-password1');
        elements.password2 = document.getElementById('register-password2');

        // Verificar que el formulario existe
        if (!elements.form) return;

        // Event listeners para validación en tiempo real
        if (elements.password1) {
            elements.password1.addEventListener('input', handlePasswordInput);
        }

        if (elements.password2) {
            elements.password2.addEventListener('input', handlePassword2Input);
        }

        if (elements.email) {
            elements.email.addEventListener('input', handleEmailInput);
        }

        // Validar campos requeridos
        [elements.firstName, elements.lastName, elements.username].forEach(element => {
            if (element) {
                element.addEventListener('input', handleRequiredFieldInput);
            }
        });

        // Handler para envío del formulario
        elements.form.addEventListener('submit', handleFormSubmit);

        // Deshabilitar validación HTML5 nativa
        elements.form.setAttribute('novalidate', 'novalidate');
    }

    // Inicializar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
