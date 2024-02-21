"use strict";
// Sample product data
const products = [
    { id: 1, name: 'Product 1', price: 10 },
    { id: 2, name: 'Product 2', price: 20 },
    { id: 3, name: 'Product 3', price: 30 },
];
// Shopping cart
const cart = [];
// Function to display products
function displayProducts() {
    const productList = document.getElementById('product-list');
    if (productList) {
        productList.innerHTML = '';
        products.forEach(product => {
            const productElement = document.createElement('div');
            productElement.classList.add('product');
            productElement.innerHTML = `
                <p>${product.name} - $${product.price}</p>
                <button onclick="addToCart(${product.id})">Add to Cart</button>
            `;
            productList.appendChild(productElement);
        });
    }
}
// Function to add a product to the shopping cart
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (product) {
        cart.push(product);
        displayShoppingCart();
    }
}
// Function to display the shopping cart
function displayShoppingCart() {
    const cartItems = document.getElementById('cart-items');
    if (cartItems) {
        cartItems.innerHTML = '';
        cart.forEach(product => {
            const cartItem = document.createElement('li');
            cartItem.innerHTML = `
                <span>${product.name} - $${product.price}</span>
            `;
            cartItems.appendChild(cartItem);
        });
    }
}
// Function to handle the checkout process (Stripe integration)
function checkout() {
    // Implement Stripe integration and payment logic here
    alert('Checkout completed!');
}
// Initial display
document.addEventListener('DOMContentLoaded', () => {
    displayProducts();
});
