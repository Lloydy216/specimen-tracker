// Enhanced JavaScript for Specimen Tracker
document.addEventListener('DOMContentLoaded', function() {
    
    // Enhanced confirmation dialogs
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('button[data-confirm]');
        if (btn) {
            const msg = btn.getAttribute('data-confirm') || 'Are you sure you want to proceed?';
            if (!window.confirm(msg)) {
                e.preventDefault();
            }
        }
    });

    // Auto-save form data to localStorage
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const formId = form.id || 'form_' + Math.random().toString(36).substr(2, 9);
        form.id = formId;
        
        // Load saved data
        const savedData = localStorage.getItem(formId);
        if (savedData) {
            try {
                const data = JSON.parse(savedData);
                Object.keys(data).forEach(key => {
                    const input = form.querySelector(`[name="${key}"]`);
                    if (input && input.type !== 'password') {
                        input.value = data[key];
                    }
                });
            } catch (e) {
                console.warn('Could not load saved form data');
            }
        }
        
        // Save data on input
        form.addEventListener('input', (e) => {
            if (e.target.name) {
                const formData = new FormData(form);
                const data = {};
                for (let [key, value] of formData.entries()) {
                    data[key] = value;
                }
                localStorage.setItem(formId, JSON.stringify(data));
            }
        });
        
        // Clear saved data on successful submit
        form.addEventListener('submit', () => {
            localStorage.removeItem(formId);
        });
    });

    // Enhanced search functionality
    const searchInputs = document.querySelectorAll('input[type="search"], input[name="q"]');
    searchInputs.forEach(input => {
        let searchTimeout;
        
        input.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // Auto-submit search after 500ms of no typing
                if (e.target.value.length > 2 || e.target.value.length === 0) {
                    const form = e.target.closest('form');
                    if (form) {
                        form.submit();
                    }
                }
            }, 500);
        });
        
        // Add search icon
        if (!input.previousElementSibling?.classList?.contains('search-icon')) {
            const searchIcon = document.createElement('span');
            searchIcon.className = 'search-icon';
            searchIcon.innerHTML = '🔍';
            searchIcon.style.cssText = 'position: absolute; left: 10px; top: 50%; transform: translateY(-50%); color: #6c757d;';
            input.parentElement.style.position = 'relative';
            input.style.paddingLeft = '35px';
            input.parentElement.insertBefore(searchIcon, input);
        }
    });

    // Enhanced table interactions
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        // Add row hover effects
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            row.addEventListener('mouseenter', () => {
                row.style.backgroundColor = '#f8fafc';
            });
            row.addEventListener('mouseleave', () => {
                row.style.backgroundColor = '';
            });
        });
        
        // Add sortable headers (basic implementation)
        const headers = table.querySelectorAll('th[data-sortable]');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {
                const column = header.cellIndex;
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));
                
                rows.sort((a, b) => {
                    const aText = a.cells[column].textContent.trim();
                    const bText = b.cells[column].textContent.trim();
                    return aText.localeCompare(bText);
                });
                
                rows.forEach(row => tbody.appendChild(row));
            });
        });
    });

    // Enhanced form validation
    const requiredFields = document.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        field.addEventListener('blur', () => {
            validateField(field);
        });
        
        field.addEventListener('input', () => {
            if (field.classList.contains('error')) {
                clearFieldError(field);
            }
        });
    });
    
    function validateField(field) {
        if (field.hasAttribute('required') && !field.value.trim()) {
            showFieldError(field, 'This field is required');
            return false;
        }
        
        if (field.type === 'email' && field.value && !isValidEmail(field.value)) {
            showFieldError(field, 'Please enter a valid email address');
            return false;
        }
        
        if (field.hasAttribute('pattern') && field.value) {
            const pattern = new RegExp(field.getAttribute('pattern'));
            if (!pattern.test(field.value)) {
                showFieldError(field, field.getAttribute('title') || 'Invalid format');
                return false;
            }
        }
        
        return true;
    }
    
    function showFieldError(field, message) {
        clearFieldError(field);
        field.classList.add('error');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.textContent = message;
        errorDiv.style.cssText = 'color: #dc3545; font-size: 0.875rem; margin-top: 0.25rem;';
        field.parentNode.appendChild(errorDiv);
    }
    
    function clearFieldError(field) {
        field.classList.remove('error');
        const errorDiv = field.parentNode.querySelector('.field-error');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
    
    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    // Enhanced accessibility
    const skipLinks = document.querySelectorAll('.skip-link');
    skipLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href').substring(1));
            if (target) {
                target.focus();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Keyboard navigation improvements
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            // Close any open modals or dropdowns
            const openDropdowns = document.querySelectorAll('.dropdown.open, .modal.open');
            openDropdowns.forEach(dropdown => {
                dropdown.classList.remove('open');
            });
        }
    });

    // Auto-focus first input in forms
    const firstInputs = document.querySelectorAll('form input:not([type="hidden"]):not([type="submit"]):not([type="button"]):not([readonly])');
    if (firstInputs.length > 0) {
        firstInputs[0].focus();
    }

    // Enhanced flash message handling
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(message => {
        // Auto-hide success messages after 5 seconds
        if (message.classList.contains('success')) {
            setTimeout(() => {
                message.style.opacity = '0';
                setTimeout(() => message.remove(), 300);
            }, 5000);
        }
        
        // Add close button to all flash messages
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '×';
        closeBtn.className = 'flash-close';
        closeBtn.style.cssText = 'background: none; border: none; color: inherit; font-size: 1.5rem; cursor: pointer; float: right; margin-left: 1rem;';
        closeBtn.addEventListener('click', () => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        });
        message.appendChild(closeBtn);
    });

    // Add smooth transitions
    const style = document.createElement('style');
    style.textContent = `
        .flash { transition: opacity 0.3s ease; }
        .card { transition: transform 0.2s ease, box-shadow 0.2s ease; }
        .btn { transition: all 0.2s ease; }
        input, select, textarea { transition: border-color 0.2s ease, box-shadow 0.2s ease; }
    `;
    document.head.appendChild(style);
});
