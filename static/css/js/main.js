// General Store Management System - Main JavaScript

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    // Auto hide alerts
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // POS System quantity validation
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const maxStock = parseInt(this.dataset.stock || 9999);
            if (this.value > maxStock) {
                alert('Not enough stock available! Maximum: ' + maxStock);
                this.value = maxStock;
            }
            if (this.value < 0) {
                this.value = 0;
            }
        });
    });
});

// POS System Functions
class POSSystem {
    constructor() {
        this.cart = [];
        this.subtotal = 0;
        this.taxRate = 0.18; // 18% GST
    }

    addToCart(productId, productName, price, stock) {
        const existingItem = this.cart.find(item => item.id === productId);
        
        if (existingItem) {
            if (existingItem.quantity < stock) {
                existingItem.quantity++;
            } else {
                this.showAlert('Not enough stock available!', 'danger');
                return;
            }
        } else {
            if (stock > 0) {
                this.cart.push({
                    id: productId,
                    name: productName,
                    price: parseFloat(price),
                    quantity: 1,
                    stock: parseInt(stock)
                });
            } else {
                this.showAlert('Product out of stock!', 'warning');
                return;
            }
        }
        
        this.updateCartDisplay();
    }

    removeFromCart(index) {
        this.cart.splice(index, 1);
        this.updateCartDisplay();
    }

    updateQuantity(index, change) {
        const item = this.cart[index];
        const newQuantity = item.quantity + change;

        if (newQuantity < 1) {
            this.removeFromCart(index);
        } else if (newQuantity > item.stock) {
            this.showAlert('Not enough stock available!', 'danger');
        } else {
            item.quantity = newQuantity;
            this.updateCartDisplay();
        }
    }

    updateCartDisplay() {
        const cartItems = document.getElementById('cartItems');
        const subtotalElem = document.getElementById('subtotal');
        const taxAmountElem = document.getElementById('taxAmount');
        const totalAmountElem = document.getElementById('totalAmount');
        const checkoutBtn = document.getElementById('checkoutBtn');

        cartItems.innerHTML = '';
        this.subtotal = 0;

        if (this.cart.length === 0) {
            cartItems.innerHTML = '<p class="text-muted text-center">Cart is empty</p>';
            if (checkoutBtn) checkoutBtn.disabled = true;
        } else {
            if (checkoutBtn) checkoutBtn.disabled = false;
            
            this.cart.forEach((item, index) => {
                const itemTotal = item.price * item.quantity;
                this.subtotal += itemTotal;

                const cartItem = document.createElement('div');
                cartItem.className = 'cart-item border-bottom pb-2 mb-2';
                cartItem.innerHTML = `
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="mb-1">${item.name}</h6>
                            <small>₹${item.price} x ${item.quantity}</small>
                        </div>
                        <div class="text-end">
                            <div class="fw-bold">₹${itemTotal.toFixed(2)}</div>
                            <div class="btn-group btn-group-sm">
                                <button type="button" class="btn btn-outline-secondary" onclick="pos.updateQuantity(${index}, -1)">-</button>
                                <button type="button" class="btn btn-outline-secondary" onclick="pos.updateQuantity(${index}, 1)">+</button>
                                <button type="button" class="btn btn-outline-danger" onclick="pos.removeFromCart(${index})">×</button>
                            </div>
                        </div>
                    </div>
                    <input type="hidden" name="product_id" value="${item.id}">
                    <input type="hidden" name="quantity" value="${item.quantity}">
                `;
                cartItems.appendChild(cartItem);
            });
        }

        const taxAmount = this.subtotal * this.taxRate;
        const totalAmount = this.subtotal + taxAmount;

        if (subtotalElem) subtotalElem.textContent = `₹${this.subtotal.toFixed(2)}`;
        if (taxAmountElem) taxAmountElem.textContent = `₹${taxAmount.toFixed(2)}`;
        if (totalAmountElem) totalAmountElem.textContent = `₹${totalAmount.toFixed(2)}`;
    }

    showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.querySelector('.messages')?.appendChild(alertDiv);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }

    clearCart() {
        this.cart = [];
        this.updateCartDisplay();
    }
}

// Initialize POS System
const pos = new POSSystem();

// Search and Filter for Products
function initializeProductSearch() {
    const searchInput = document.getElementById('searchProduct');
    const categoryFilter = document.getElementById('categoryFilter');
    
    if (searchInput && categoryFilter) {
        searchInput.addEventListener('input', filterProducts);
        categoryFilter.addEventListener('change', filterProducts);
    }
}

function filterProducts() {
    const searchTerm = document.getElementById('searchProduct')?.value.toLowerCase() || '';
    const categoryFilter = document.getElementById('categoryFilter')?.value || '';
    
    document.querySelectorAll('.product-item').forEach(item => {
        const productName = item.querySelector('.card-title')?.textContent.toLowerCase() || '';
        const productCategory = item.dataset.category || '';
        
        const matchesSearch = productName.includes(searchTerm);
        const matchesCategory = !categoryFilter || productCategory === categoryFilter;
        
        item.style.display = (matchesSearch && matchesCategory) ? 'block' : 'none';
    });
}

// Initialize when document is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeProductSearch();
    
    // Add to cart buttons event listeners
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.product-card');
            const productId = card.dataset.productId;
            const productName = card.dataset.productName;
            const productPrice = card.dataset.productPrice;
            const productStock = card.dataset.productStock;
            
            pos.addToCart(productId, productName, productPrice, productStock);
        });
    });
});

// Print functionality
function printInvoice() {
    window.print();
}

// Export functions to global scope
window.pos = pos;
window.printInvoice = printInvoice;
window.filterProducts = filterProducts;
