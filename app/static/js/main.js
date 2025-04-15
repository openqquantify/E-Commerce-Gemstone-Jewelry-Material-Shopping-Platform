// Main JavaScript for Gemstone Marketplace
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Product image hover effect
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            const img = card.querySelector('.product-image');
            if (img) {
                img.style.transform = 'scale(1.05)';
            }
        });
        card.addEventListener('mouseleave', () => {
            const img = card.querySelector('.product-image');
            if (img) {
                img.style.transform = 'scale(1)';
            }
        });
    });

    // Password strength indicator for registration form
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            const strengthIndicator = document.getElementById('password-strength');
            const strength = calculatePasswordStrength(this.value);
            
            strengthIndicator.textContent = strength.text;
            strengthIndicator.className = 'password-strength ' + strength.class;
        });
    }

    // Image preview for product uploads
    const imageUpload = document.getElementById('image');
    if (imageUpload) {
        imageUpload.addEventListener('change', function() {
            const preview = document.getElementById('image-preview');
            const file = this.files[0];
            
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.innerHTML = `
                        <img src="${e.target.result}" class="img-fluid rounded mt-2" style="max-height: 200px;">
                        <small class="d-block text-muted mt-1">${file.name}</small>
                    `;
                }
                reader.readAsDataURL(file);
            } else {
                preview.innerHTML = '';
            }
        });
    }

    // Shopping cart counter
    updateCartCounter();
});

function calculatePasswordStrength(password) {
    const strength = {
        text: 'Weak',
        class: 'weak'
    };
    
    if (password.length >= 12) {
        strength.text = 'Very Strong';
        strength.class = 'very-strong';
    } else if (password.length >= 8) {
        strength.text = 'Strong';
        strength.class = 'strong';
    } else if (password.length >= 5) {
        strength.text = 'Medium';
        strength.class = 'medium';
    }
    
    return strength;
}

function updateCartCounter() {
    const cartCounter = document.getElementById('cart-counter');
    if (cartCounter) {
        // In a real app, you would fetch this from your backend/session
        const cartItems = JSON.parse(localStorage.getItem('cart')) || [];
        cartCounter.textContent = cartItems.length;
        cartCounter.style.display = cartItems.length ? 'inline-block' : 'none';
    }
}

// Stripe payment handler (would be called from checkout page)
function handlePayment() {
    // This would be replaced with actual Stripe.js implementation
    console.log('Payment processing...');
    // In production, you would use Stripe.js elements here
}

// Utility function for AJAX requests
function makeRequest(url, method, data, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 300) {
            callback(null, JSON.parse(xhr.responseText));
        } else {
            callback(xhr.statusText, null);
        }
    };
    xhr.onerror = function() {
        callback('Network error', null);
    };
    xhr.send(JSON.stringify(data));
}
