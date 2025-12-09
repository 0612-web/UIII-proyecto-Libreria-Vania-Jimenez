// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Animación para cards
    const cards = document.querySelectorAll('.libro-card, .card');
    cards.forEach(card => {
        card.classList.add('animated');
    });
    
    // Actualizar cantidad en carrito
    const quantityInputs = document.querySelectorAll('.quantity-input');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const itemId = this.dataset.itemId;
            const newQuantity = this.value;
            
            if (newQuantity > 0 && newQuantity <= 10) {
                updateCartItem(itemId, newQuantity);
            }
        });
    });
    
    // Validación de formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = this.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                    
                    // Crear mensaje de error si no existe
                    if (!field.nextElementSibling || !field.nextElementSibling.classList.contains('invalid-feedback')) {
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'invalid-feedback';
                        errorDiv.textContent = 'Este campo es requerido';
                        field.parentNode.appendChild(errorDiv);
                    }
                } else {
                    field.classList.remove('is-invalid');
                    const errorDiv = field.nextElementSibling;
                    if (errorDiv && errorDiv.classList.contains('invalid-feedback')) {
                        errorDiv.remove();
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                // Mostrar alerta
                showAlert('Por favor, completa todos los campos requeridos.', 'danger');
            }
        });
    });
    
    // Funciones de ayuda
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
            
            // Auto-remover después de 5 segundos
            setTimeout(() => {
                alertDiv.remove();
            }, 5000);
        }
    }
    
    function updateCartItem(itemId, quantity) {
        // Esta función se implementará cuando tengamos las APIs
        console.log(`Actualizando item ${itemId} a cantidad ${quantity}`);
    }
    
    // Efecto hover para cards
    const hoverCards = document.querySelectorAll('.card-hover');
    hoverCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Función para agregar al carrito
    window.addToCart = function(libroId) {
        console.log(`Agregando libro ${libroId} al carrito`);
        showAlert('Producto agregado al carrito', 'success');
    };
    
    // Función para remover del carrito
    window.removeFromCart = function(itemId) {
        if (confirm('¿Estás seguro de que quieres eliminar este item del carrito?')) {
            console.log(`Removiendo item ${itemId} del carrito`);
            showAlert('Producto removido del carrito', 'warning');
        }
    };
});