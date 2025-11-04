/**
 * ========================================
 * JAVASCRIPT DEL DASHBOARD
 * Archivo: dashboard.js
 * ========================================
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // Active Menu Item
    // ==========================================
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        if (item.getAttribute('href') === currentPath) {
            menuItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
        }
    });
    
    // ==========================================
    // Auto-refresh Statistics (opcional)
    // ==========================================
    function refreshStats() {
        // Aquí podrías hacer peticiones AJAX para actualizar estadísticas
        console.log('Actualizando estadísticas...');
    }
    
    // Actualizar cada 60 segundos
    // setInterval(refreshStats, 60000);
    
    // ==========================================
    // Tooltips
    // ==========================================
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
});
