// Resume Interactive Features

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive features
    initializeSkillAnimations();
    initializeNavigation();
    initializeContactForm();
    initializePrintOptimization();
    
    console.log('Resume application initialized');
});

// Skill Progress Bar Animations
function initializeSkillAnimations() {
    const skillBars = document.querySelectorAll('.skill-progress .progress-bar');
    
    // Create intersection observer for skill animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const proficiency = progressBar.getAttribute('data-proficiency');
                
                // Animate the progress bar
                setTimeout(() => {
                    progressBar.style.width = proficiency + '%';
                }, 200);
                
                // Unobserve after animation
                observer.unobserve(progressBar);
            }
        });
    }, {
        threshold: 0.5,
        rootMargin: '0px 0px -50px 0px'
    });
    
    // Observe all skill progress bars
    skillBars.forEach(bar => {
        bar.style.width = '0%'; // Start with 0 width
        observer.observe(bar);
    });
}

// Smooth Navigation and Active States
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link[href^="#"]');
    const sections = document.querySelectorAll('section[id]');
    
    // Smooth scrolling for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                const navbarHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = targetSection.offsetTop - navbarHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Update active navigation state on scroll
    window.addEventListener('scroll', throttle(() => {
        let current = '';
        const scrollPosition = window.scrollY + 100;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });
        
        // Update active nav link
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    }, 100));
}

// Contact Form Enhancements
function initializeContactForm() {
    const contactForm = document.querySelector('#contact form');
    
    if (contactForm) {
        // Form validation enhancement
        contactForm.addEventListener('submit', function(e) {
            const name = this.querySelector('#name').value.trim();
            const email = this.querySelector('#email').value.trim();
            const message = this.querySelector('#message').value.trim();
            
            if (!name || !email || !message) {
                e.preventDefault();
                showAlert('Please fill in all required fields.', 'danger');
                return;
            }
            
            if (!isValidEmail(email)) {
                e.preventDefault();
                showAlert('Please enter a valid email address.', 'danger');
                return;
            }
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
            submitBtn.disabled = true;
            
            // Re-enable button after a delay (form will redirect anyway)
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 3000);
        });
        
        // Auto-resize textarea
        const messageTextarea = contactForm.querySelector('#message');
        if (messageTextarea) {
            messageTextarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = (this.scrollHeight) + 'px';
            });
        }
    }
}

// Print Optimization
function initializePrintOptimization() {
    // Add print-specific classes before printing
    window.addEventListener('beforeprint', function() {
        document.body.classList.add('printing');
        
        // Expand all collapsed elements for print
        const collapseElements = document.querySelectorAll('.collapse:not(.show)');
        collapseElements.forEach(el => {
            el.classList.add('show');
            el.setAttribute('data-was-collapsed', 'true');
        });
    });
    
    // Remove print-specific classes after printing
    window.addEventListener('afterprint', function() {
        document.body.classList.remove('printing');
        
        // Restore collapsed state
        const expandedElements = document.querySelectorAll('[data-was-collapsed="true"]');
        expandedElements.forEach(el => {
            el.classList.remove('show');
            el.removeAttribute('data-was-collapsed');
        });
    });
}

// Utility Functions
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Find or create alert container
    let alertContainer = document.querySelector('.alert-container');
    if (!alertContainer) {
        alertContainer = document.createElement('div');
        alertContainer.className = 'alert-container position-fixed top-0 start-50 translate-middle-x';
        alertContainer.style.zIndex = '9999';
        alertContainer.style.marginTop = '80px';
        document.body.appendChild(alertContainer);
    }
    
    // Add alert to container
    alertContainer.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Project Card Interactions
document.addEventListener('DOMContentLoaded', function() {
    const projectCards = document.querySelectorAll('.project-card');
    
    projectCards.forEach(card => {
        // Add hover effect for project links
        const projectLinks = card.querySelectorAll('.project-links a');
        projectLinks.forEach(link => {
            link.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.05)';
            });
            
            link.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
            });
        });
    });
});

// Admin Form Enhancements
if (window.location.pathname.includes('/admin')) {
    document.addEventListener('DOMContentLoaded', function() {
        // Auto-focus first form field
        const firstFormField = document.querySelector('form input:not([type="hidden"]), form textarea, form select');
        if (firstFormField) {
            firstFormField.focus();
        }
        
        // Confirm delete actions
        const deleteButtons = document.querySelectorAll('button[onclick*="confirm"]');
        deleteButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                    e.preventDefault();
                    return false;
                }
            });
        });
        
        // Auto-save form data to localStorage (recovery feature)
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            const formId = form.action + '_' + (form.method || 'get');
            
            // Load saved data
            const savedData = localStorage.getItem(formId);
            if (savedData) {
                try {
                    const data = JSON.parse(savedData);
                    Object.keys(data).forEach(key => {
                        const field = form.querySelector(`[name="${key}"]`);
                        if (field && field.type !== 'hidden') {
                            if (field.type === 'checkbox') {
                                field.checked = data[key];
                            } else {
                                field.value = data[key];
                            }
                        }
                    });
                } catch (e) {
                    console.warn('Could not restore form data:', e);
                }
            }
            
            // Save data on input
            form.addEventListener('input', throttle(function() {
                const formData = new FormData(form);
                const data = {};
                for (let [key, value] of formData.entries()) {
                    if (key !== 'csrf_token') {
                        data[key] = value;
                    }
                }
                localStorage.setItem(formId, JSON.stringify(data));
            }, 1000));
            
            // Clear saved data on successful submit
            form.addEventListener('submit', function() {
                localStorage.removeItem(formId);
            });
        });
    });
}

// Skills Chart Animation (if Chart.js is loaded)
function animateSkillsChart() {
    const chartCanvas = document.getElementById('skillsChart');
    if (chartCanvas && window.Chart) {
        // Create intersection observer for chart
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Chart will be created by the template script
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.3
        });
        
        observer.observe(chartCanvas);
    }
}

// Initialize chart animation
document.addEventListener('DOMContentLoaded', animateSkillsChart);

// Responsive table handling
function initializeResponsiveTables() {
    const tables = document.querySelectorAll('.table-responsive table');
    
    tables.forEach(table => {
        // Add mobile-friendly scrolling hints
        const container = table.closest('.table-responsive');
        if (container) {
            container.addEventListener('scroll', function() {
                const scrollLeft = this.scrollLeft;
                const scrollWidth = this.scrollWidth;
                const clientWidth = this.clientWidth;
                
                // Add classes for scroll indicators
                this.classList.toggle('scrolled-left', scrollLeft > 0);
                this.classList.toggle('scrolled-right', scrollLeft < scrollWidth - clientWidth - 1);
            });
        }
    });
}

// Initialize responsive tables
document.addEventListener('DOMContentLoaded', initializeResponsiveTables);
