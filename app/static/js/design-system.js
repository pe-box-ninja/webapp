// Modal functionality
function initializeModals() {
    document.querySelectorAll('[data-toggle="modal"]').forEach(button => {
        const targetId = button.getAttribute('data-target');
        const modal = document.getElementById(targetId);
        const closeButton = modal.querySelector('.close');
        const footerCloseButton = modal.querySelector('.modal-footer .btn-secondary');

        button.addEventListener('click', () => {
            modal.style.display = 'block';
        });

        const closeModal = () => {
            modal.style.display = 'none';
        };

        if (closeButton) {
            closeButton.addEventListener('click', closeModal);
        }

        if (footerCloseButton) {
            footerCloseButton.addEventListener('click', closeModal);
        }

        window.addEventListener('click', (event) => {
            if (event.target === modal) {
                closeModal();
            }
        });
    });
}

// Tooltip functionality
function initializeTooltips() {
    document.querySelectorAll('[data-toggle="tooltip"]').forEach(element => {
        new bootstrap.Tooltip(element);
    });
}

// Tab functionality
function initializeTabs() {
    document.querySelectorAll('.nav-tabs .nav-link').forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            const tabId = tab.getAttribute('data-bs-target');
            const tabContent = document.querySelector(tabId);
            
            // Remove active class from all tabs and content
            tab.closest('.nav-tabs').querySelectorAll('.nav-link').forEach(t => t.classList.remove('active'));
            tab.closest('.tab-content').querySelectorAll('.tab-pane').forEach(p => p.classList.remove('show', 'active'));
            
            // Add active class to clicked tab and its content
            tab.classList.add('active');
            tabContent.classList.add('show', 'active');
        });
    });
}

// Accordion functionality
function initializeAccordions() {
    document.querySelectorAll('.accordion-button').forEach(button => {
        button.addEventListener('click', () => {
            const target = document.querySelector(button.getAttribute('data-bs-target'));
            if (target) {
                target.classList.toggle('show');
                button.classList.toggle('collapsed');
                const expanded = button.getAttribute('aria-expanded') === 'true';
                button.setAttribute('aria-expanded', !expanded);
            }
        });
    });
}

// Initialize all components
document.addEventListener('DOMContentLoaded', () => {
    initializeModals();
    initializeTooltips();
    initializeTabs();
    initializeAccordions();
});