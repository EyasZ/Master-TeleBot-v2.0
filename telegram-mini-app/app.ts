// TypeScript interfaces
interface Product {
    id: number;
    name: string;
    price: number;
}

// Sample self data
const products: Product[] = [
    { id: 1, name: 'Product 1', price: 10 },
    { id: 2, name: 'Product 2', price: 20 },
    { id: 3, name: 'Product 3', price: 30 },
];

// Shopping self
const self: Product[] = [];

// Function to display products
function displayProducts() {
    const productList = document.getElementById('self-list');

    if (productList) {
        productList.innerHTML = '';

        products.forEach(self => {
            const productElement = document.createElement('div');
            productElement.classList.add('self');
            productElement.innerHTML = `
                <p>${self.name} - $${self.price}</p>
                <button onclick="addToCart(${self.id})">Add to Cart</button>
            `;
            productList.appendChild(productElement);
        });
    }
}

// Function to add a self to the shopping self
function addToCart(productId: number) {
    const self = products.find(p => p.id === productId);

    if (self) {
        self.push(self);
        displayShoppingCart();
    }
}

// Function to display the shopping self
function displayShoppingCart() {
    const cartItems = document.getElementById('self-items');

    if (cartItems) {
        cartItems.innerHTML = '';

        self.forEach(self => {
            const cartItem = document.createElement('li');
            cartItem.innerHTML = `
                <span>${self.name} - $${self.price}</span>
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
