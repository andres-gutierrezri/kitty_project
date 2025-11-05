/**
 * ========================================
 * SISTEMA DE MODALES PERSONALIZADOS
 * Archivo: customModals.js
 * ========================================
 * 
 * Sistema centralizado de modales para reemplazar alert(), confirm()
 * y otras notificaciones nativas del navegador con modales Bootstrap
 * personalizados que siguen el estilo del proyecto.
 */

(function() {
    'use strict';

    /**
     * Crea el contenedor de modales si no existe
     */
    function createModalContainer() {
        let container = document.getElementById('custom-modals-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'custom-modals-container';
            container.setAttribute('aria-live', 'polite');
            container.setAttribute('aria-atomic', 'true');
            document.body.appendChild(container);
        }
        return container;
    }

    /**
     * Genera un ID único para cada modal
     */
    function generateModalId() {
        return 'customModal-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
    }

    /**
     * Obtiene el icono y color según el tipo de modal
     */
    function getModalStyle(type) {
        const styles = {
            success: {
                icon: 'fa-check-circle',
                color: 'text-success',
                bgColor: 'bg-success',
                title: '✅ Éxito'
            },
            error: {
                icon: 'fa-times-circle',
                color: 'text-danger',
                bgColor: 'bg-danger',
                title: '❌ Error'
            },
            warning: {
                icon: 'fa-exclamation-triangle',
                color: 'text-warning',
                bgColor: 'bg-warning',
                title: '⚠️ Advertencia'
            },
            info: {
                icon: 'fa-info-circle',
                color: 'text-info',
                bgColor: 'bg-info',
                title: 'ℹ️ Información'
            },
            confirm: {
                icon: 'fa-question-circle',
                color: 'text-primary',
                bgColor: 'bg-primary',
                title: '❓ Confirmación'
            }
        };
        return styles[type] || styles.info;
    }

    /**
     * Crea el HTML del modal
     */
    function createModalHTML(id, title, message, type, options = {}) {
        const style = getModalStyle(type);
        const showCancel = options.showCancel || false;
        const confirmText = options.confirmText || 'Aceptar';
        const cancelText = options.cancelText || 'Cancelar';
        const customTitle = options.title || style.title;

        return `
            <div class="modal fade" id="${id}" tabindex="-1" aria-labelledby="${id}Label" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content border-0 shadow-lg">
                        <div class="modal-header ${style.bgColor} text-white border-0">
                            <h5 class="modal-title d-flex align-items-center" id="${id}Label">
                                <i class="fas ${style.icon} me-2"></i>
                                <span>${customTitle}</span>
                            </h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Cerrar"></button>
                        </div>
                        <div class="modal-body py-4">
                            <div class="d-flex align-items-start">
                                <i class="fas ${style.icon} ${style.color} fs-1 me-3 mt-1"></i>
                                <div class="flex-grow-1">
                                    <p class="mb-0" style="font-size: 1.1rem;">${message}</p>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer border-0 bg-light">
                            ${showCancel ? `
                                <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">
                                    <i class="fas fa-times me-1"></i> ${cancelText}
                                </button>
                            ` : ''}
                            <button type="button" class="btn btn-${type === 'error' ? 'danger' : type === 'warning' ? 'warning' : type === 'success' ? 'success' : 'primary'} custom-modal-confirm">
                                <i class="fas fa-check me-1"></i> ${confirmText}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Muestra un modal personalizado
     */
    function showModal(message, type = 'info', options = {}) {
        return new Promise((resolve) => {
            const container = createModalContainer();
            const modalId = generateModalId();
            const title = options.title || '';
            
            // Crear el HTML del modal
            const modalHTML = createModalHTML(modalId, title, message, type, options);
            container.insertAdjacentHTML('beforeend', modalHTML);
            
            // Obtener el elemento del modal
            const modalElement = document.getElementById(modalId);
            const modal = new bootstrap.Modal(modalElement);
            
            // Configurar eventos
            const confirmBtn = modalElement.querySelector('.custom-modal-confirm');
            
            // Handler para confirmar
            const handleConfirm = () => {
                modal.hide();
                resolve(true);
            };
            
            // Handler para cancelar
            const handleCancel = () => {
                modal.hide();
                resolve(false);
            };
            
            // Agregar event listeners
            confirmBtn.addEventListener('click', handleConfirm);
            
            if (options.showCancel) {
                const cancelBtn = modalElement.querySelector('[data-bs-dismiss="modal"]');
                if (cancelBtn) {
                    cancelBtn.addEventListener('click', handleCancel);
                }
            }
            
            // Limpiar el modal del DOM después de cerrarlo
            modalElement.addEventListener('hidden.bs.modal', function() {
                modalElement.remove();
            });
            
            // Mostrar el modal
            modal.show();
            
            // Auto-cerrar en modo alerta (sin confirmación)
            if (!options.showCancel && options.autoClose !== false) {
                // Focus en el botón de confirmar
                modalElement.addEventListener('shown.bs.modal', function() {
                    confirmBtn.focus();
                });
            }
        });
    }

    /**
     * API Pública - Modal de Alerta
     * Reemplazo directo de alert()
     */
    window.showAlert = function(message, type = 'info', options = {}) {
        return showModal(message, type, { ...options, showCancel: false });
    };

    /**
     * API Pública - Modal de Confirmación
     * Reemplazo directo de confirm()
     */
    window.showConfirm = function(message, options = {}) {
        return showModal(message, 'confirm', { ...options, showCancel: true });
    };

    /**
     * API Pública - Modal de Éxito
     */
    window.showSuccess = function(message, options = {}) {
        return showModal(message, 'success', { ...options, showCancel: false });
    };

    /**
     * API Pública - Modal de Error
     */
    window.showError = function(message, options = {}) {
        return showModal(message, 'error', { ...options, showCancel: false });
    };

    /**
     * API Pública - Modal de Advertencia
     */
    window.showWarning = function(message, options = {}) {
        return showModal(message, 'warning', { ...options, showCancel: false });
    };

    /**
     * API Pública - Modal de Información
     */
    window.showInfo = function(message, options = {}) {
        return showModal(message, 'info', { ...options, showCancel: false });
    };

    /**
     * Reemplazo global de alert() nativo
     * Comentar esta línea si se desea mantener alert() nativo
     */
    // window.alert = function(message) {
    //     showAlert(message, 'info');
    // };

    /**
     * Reemplazo global de confirm() nativo
     * Comentar esta línea si se desea mantener confirm() nativo
     */
    // window.confirm = function(message) {
    //     return showConfirm(message);
    // };

    console.log('✅ Sistema de modales personalizados cargado correctamente');

})();

