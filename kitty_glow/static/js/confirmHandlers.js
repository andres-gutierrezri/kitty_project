/**
 * ========================================
 * MANEJADORES DE CONFIRMACIÓN
 * Archivo: confirmHandlers.js
 * ========================================
 * 
 * Reemplaza las confirmaciones inline en formularios HTML
 * con modales personalizados de Bootstrap.
 */

(function() {
    'use strict';

    /**
     * Maneja las confirmaciones de formularios con data-confirm
     */
    function initializeFormConfirmations() {
        // Buscar todos los formularios con atributo data-confirm
        document.querySelectorAll('form[data-confirm]').forEach(form => {
            form.addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const message = this.getAttribute('data-confirm');
                const title = this.getAttribute('data-confirm-title') || '❓ Confirmación';
                const confirmText = this.getAttribute('data-confirm-text') || 'Sí, continuar';
                const cancelText = this.getAttribute('data-cancel-text') || 'No, cancelar';
                const type = this.getAttribute('data-confirm-type') || 'confirm';
                
                const confirmed = await showConfirm(message, {
                    title: title,
                    confirmText: confirmText,
                    cancelText: cancelText
                });
                
                if (confirmed) {
                    // Remover el listener temporalmente para evitar loop
                    this.removeEventListener('submit', arguments.callee);
                    this.submit();
                }
            });
        });
    }

    /**
     * Maneja las confirmaciones de botones con data-confirm
     */
    function initializeButtonConfirmations() {
        // Buscar todos los botones con atributo data-confirm
        document.querySelectorAll('button[data-confirm], a[data-confirm]').forEach(element => {
            element.addEventListener('click', async function(e) {
                e.preventDefault();
                
                const message = this.getAttribute('data-confirm');
                const title = this.getAttribute('data-confirm-title') || '❓ Confirmación';
                const confirmText = this.getAttribute('data-confirm-text') || 'Sí, continuar';
                const cancelText = this.getAttribute('data-cancel-text') || 'No, cancelar';
                
                const confirmed = await showConfirm(message, {
                    title: title,
                    confirmText: confirmText,
                    cancelText: cancelText
                });
                
                if (confirmed) {
                    // Si es un botón de formulario, enviar el formulario
                    if (this.type === 'submit' && this.form) {
                        this.form.submit();
                    }
                    // Si es un enlace, navegar
                    else if (this.tagName === 'A') {
                        window.location.href = this.href;
                    }
                }
            });
        });
    }

    /**
     * Inicializa todos los manejadores cuando el DOM esté listo
     */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initializeFormConfirmations();
            initializeButtonConfirmations();
        });
    } else {
        initializeFormConfirmations();
        initializeButtonConfirmations();
    }

    // Exportar funciones para uso manual si es necesario
    window.ConfirmHandlers = {
        reinitialize: function() {
            initializeFormConfirmations();
            initializeButtonConfirmations();
        }
    };

    console.log('✅ Manejadores de confirmación cargados correctamente');

})();

