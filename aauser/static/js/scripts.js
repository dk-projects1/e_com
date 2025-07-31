// Initialize cart from localStorage
let cart = JSON.parse(localStorage.getItem('cart')) || {};

// Save cart to localStorage
function saveCart() {
  localStorage.setItem('cart', JSON.stringify(cart));
}

// Add to cart handler
function addToCart(button) {
  const card = button.closest('.product-card');
  const id = card.getAttribute('data-id');
  const name = card.getAttribute('data-name');
  const price = parseInt(card.getAttribute('data-price'));
  const img = card.getAttribute('data-img');

  const size = document.getElementById('size').value;
  const qty = parseInt(document.getElementById('quantity').value);

  if (!size) {
    alert("Please select a size.");
    return;
  }

  const key = `${id}_${size}`;

  if (!cart[key]) {
    cart[key] = { id, name, price, img, qty, size };
  } else {
    cart[key].qty += qty;
  }

  saveCart();
  updateCart();
}

// Remove an item from cart
function removeFromCart(key) {
  delete cart[key];
  saveCart();
  updateCart();
}

// Increase or decrease quantity
function changeQty(key, delta) {
  if (cart[key]) {
    cart[key].qty += delta;
    if (cart[key].qty <= 0) {
      delete cart[key];
    }
    saveCart();
    updateCart();
  }
}

// Update cart HTML in sidebar
function updateCart() {
  const cartItems = document.getElementById("cartItems");
  cartItems.innerHTML = '';
  let total = 0;
  let count = 0;

  for (let key in cart) {
    const item = cart[key];
    const price = item.price * item.qty;
    total += price;
    count += item.qty;

    cartItems.innerHTML += `
      <div class="cart-product">
        <img src="${item.img}" alt="${item.name}" />
        <div class="cart-info">
          <span>${item.name}</span>
          <small>(Size: ${item.size})</small>
          <div class="mini">₹${item.price} × ${item.qty}</div>
          <div class="cart-controls">
            <button onclick="changeQty('${key}', -1)">−</button>
            <button onclick="changeQty('${key}', 1)">+</button>
            <button class="remove-btn" onclick="removeFromCart('${key}')">×</button>
          </div>
        </div>
        <div class="prod-total">₹${price}</div>
      </div>
    `;
  }

  document.getElementById("cartTotal").innerText = "₹" + total;
  const cartCount = document.getElementById("cartCount");
  if (cartCount) {
    cartCount.innerText = count;
  }
}

// Show/hide cart
function openCart() {
  document.getElementById("cartSidebar").style.display = "flex";
}

function closeCart() {
  document.getElementById("cartSidebar").style.display = "none";
}

// Size selection logic
function selectSize(button) {
  document.querySelectorAll('.size-option').forEach(btn => btn.classList.remove('active'));
  button.classList.add('active');
  document.getElementById('size').value = button.dataset.size;
}

// Get CSRF token from cookies
function getCSRFToken() {
  const name = "csrftoken=";
  const decoded = decodeURIComponent(document.cookie);
  const cookies = decoded.split(";");
  for (let i = 0; i < cookies.length; i++) {
    let cookie = cookies[i].trim();
    if (cookie.startsWith(name)) return cookie.substring(name.length);
  }
  return "";
}

// Handle mobile menu toggle
function toggleMobileMenu() {
  const menu = document.getElementById('navMenu');
  menu.classList.toggle('active');
}

// Dropdown toggle (for mobile)
function toggleDropdown(element) {
  if (window.innerWidth <= 768) {
    element.classList.toggle('open');
  }
}

// Close dropdowns when clicking outside
document.addEventListener("click", function (e) {
  document.querySelectorAll(".dropdown").forEach(drop => {
    if (!drop.contains(e.target)) {
      drop.classList.remove("open");
    }
  });
});


function toggleMobileMenu() {
  const menu = document.getElementById('navMenu');
  menu.classList.toggle('active');
}

function toggleDropdown(element) {
  if (window.innerWidth <= 768) {
    element.classList.toggle('open');
  }
}

document.addEventListener("click", function (e) {
  document.querySelectorAll(".dropdown").forEach(drop => {
    if (!drop.contains(e.target)) {
      drop.classList.remove("open");
    }
  });
});

// Size selection logic
// function selectSize(button) {
//   document.querySelectorAll('.size-option').forEach(btn => btn.classList.remove('active'));
//   button.classList.add('active');
//   document.getElementById('size').value = button.dataset.size;
// }
