// --- UI helpers ---

function showLoading() {
    document.getElementById('menu-loading').hidden = false;
    document.getElementById('menu-grid').hidden = true;
    document.getElementById('menu-error').hidden = true;
}

function hideLoading() {
    document.getElementById('menu-loading').hidden = true;
}

function showError(msg) {
    document.getElementById('menu-error').textContent = msg;
    document.getElementById('menu-error').hidden = false;
}

function formatPrice(price) {
    return Number(price).toLocaleString('es-AR', {
        style: 'currency',
        currency: 'ARS',
        minimumFractionDigits: 0,
    });
}

// --- Renderizado ---

function renderCard(dish) {
    const article = document.createElement('article');
    article.className = 'dish-card';

    const imageHtml = dish.image_url
        ? `<img src="${dish.image_url}" alt="${dish.name}" loading="lazy">`
        : `<div class="dish-img-placeholder">🍽</div>`;

    article.innerHTML = `
        ${imageHtml}
        <div class="dish-card-body">
            <h2 class="dish-name">${dish.name}</h2>
            <p class="dish-description">${dish.description || ''}</p>
            <span class="dish-price">${formatPrice(dish.price)}</span>
            
            <button class="add-to-cart-btn" 
                data-id="${dish.id || dish.name}" 
                data-name="${dish.name}" 
                data-price="${dish.price}">
                Agregar al carrito
            </button>
        </div>
    `;
    return article;
}

function renderCards(dishes) {
    const grid = document.getElementById('menu-grid');
    grid.innerHTML = '';

    if (dishes.length === 0) {
        grid.innerHTML = '<p class="empty-message">No hay platos en esta categoría.</p>';
    } else {
        dishes.forEach(dish => grid.appendChild(renderCard(dish)));
    }

    grid.hidden = false;
}

function buildTabs(dishes) {
    const tabsContainer = document.getElementById('menu-tabs');
    const categories = [...new Set(dishes.map(d => d.category))].sort();

    tabsContainer.innerHTML = '';

    const allBtn = document.createElement('button');
    allBtn.className = 'tab-btn active';
    allBtn.dataset.category = 'all';
    allBtn.setAttribute('role', 'tab');
    allBtn.setAttribute('aria-selected', 'true');
    allBtn.textContent = 'Todos';
    tabsContainer.appendChild(allBtn);

    categories.forEach(cat => {
        const btn = document.createElement('button');
        btn.className = 'tab-btn';
        btn.dataset.category = cat;
        btn.setAttribute('role', 'tab');
        btn.setAttribute('aria-selected', 'false');
        btn.textContent = cat.charAt(0).toUpperCase() + cat.slice(1);
        tabsContainer.appendChild(btn);
    });

    tabsContainer.addEventListener('click', e => {
        const btn = e.target.closest('.tab-btn');
        if (!btn) return;
        setActiveTab(btn);
        fetchDishes(btn.dataset.category);
    });
}

function setActiveTab(clickedBtn) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        btn.setAttribute('aria-selected', 'false');
    });
    clickedBtn.classList.add('active');
    clickedBtn.setAttribute('aria-selected', 'true');
}

// --- Fetch ---

async function fetchDishes(category) {
    showLoading();

    const url = category === 'all'
        ? '/menu/dishes'
        : `/menu/dishes?category=${category}`;

    try {
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const dishes = await res.json();
        renderCards(dishes);
    } catch {
        showError('No se pudo cargar el menú. Verificá que el servidor esté activo.');
    } finally {
        hideLoading();
    }
}

// --- Estado Global del Carrito ---
let cart = [];

// --- Init y Lógica de Eventos ---

document.addEventListener('DOMContentLoaded', async () => {
    
    // ==========================================
    // 1. CARGAR EL MENÚ AL ENTRAR A LA PÁGINA
    // ==========================================
    showLoading();
    try {
        const res = await fetch('/menu/dishes');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const dishes = await res.json();
        buildTabs(dishes);
        renderCards(dishes);
    } catch {
        showError('No se pudo cargar el menú. Verificá que el servidor esté activo.');
    } finally {
        hideLoading();
    }

    // ==========================================
    // 2. LÓGICA DEL CARRITO DE COMPRAS
    // ==========================================
    const cartFloatBtn = document.getElementById('cart-float-btn');
    const cartModal = document.getElementById('cart-modal');
    const closeCartBtn = document.getElementById('close-cart-btn');
    const btnPay = document.getElementById('btn-pay');
    
    const cartItemsList = document.getElementById('cart-items-list');
    const emptyCartMsg = document.getElementById('empty-cart-msg');
    const cartTotalContainer = document.getElementById('cart-total-container');
    const cartTotalPrice = document.getElementById('cart-total-price');

    // Función para mostrar/ocultar el modal
    function toggleCartModal() {
        if(cartModal) cartModal.hidden = !cartModal.hidden;
    }

    if(cartFloatBtn) cartFloatBtn.addEventListener('click', toggleCartModal);
    if(closeCartBtn) closeCartBtn.addEventListener('click', toggleCartModal);
    if(cartModal) {
        cartModal.addEventListener('click', (e) => {
            if (e.target === cartModal) toggleCartModal();
        });
    }

    // Función para actualizar el HTML del carrito
    function updateCartUI() {
        cartItemsList.innerHTML = '';
        let total = 0;

        if (cart.length === 0) {
            emptyCartMsg.hidden = false;
            cartTotalContainer.hidden = true;
        } else {
            emptyCartMsg.hidden = true;
            cartTotalContainer.hidden = false;

            cart.forEach((item, index) => {
                total += item.price;
                const li = document.createElement('li');
                li.className = 'cart-item';
                li.innerHTML = `
                    <div class="cart-item-info">
                        <span class="cart-item-title">${item.name}</span>
                        <span class="cart-item-price">${formatPrice(item.price)}</span>
                    </div>
                    <button class="remove-item-btn" data-index="${index}">&times;</button>
                `;
                cartItemsList.appendChild(li);
            });
        }

        cartTotalPrice.textContent = formatPrice(total);
    }

    // Escuchar clics en "Agregar al carrito" (Delegación de eventos en el grid)
    const menuGrid = document.getElementById('menu-grid');
    if(menuGrid) {
        menuGrid.addEventListener('click', (e) => {
            if (e.target.classList.contains('add-to-cart-btn')) {
                const btn = e.target;
                const item = {
                    id: btn.getAttribute('data-id'),
                    name: btn.getAttribute('data-name'),
                    price: parseFloat(btn.getAttribute('data-price'))
                };
                
                cart.push(item);
                updateCartUI();
                
                // Feedback visual en el botón
                const originalText = btn.textContent;
                btn.textContent = "¡Agregado!";
                btn.style.backgroundColor = "#dd9755";
                btn.style.color = "#111";
                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.style.backgroundColor = "transparent";
                    btn.style.color = "#dd9755";
                }, 1000);
            }
        });
    }

    // Eliminar items del carrito
    if(cartItemsList) {
        cartItemsList.addEventListener('click', (e) => {
            if (e.target.classList.contains('remove-item-btn')) {
                const index = e.target.getAttribute('data-index');
                cart.splice(index, 1);
                updateCartUI();
            }
        });
    }

    // Simulación del botón Pagar
    if(btnPay) {
        btnPay.addEventListener('click', () => {
            if (cart.length === 0) {
                if (typeof Swal !== 'undefined') {
                    Swal.fire({
                        title: 'Carrito vacío',
                        text: 'Agrega algunos platos antes de pagar.',
                        icon: 'warning',
                        confirmButtonText: 'Aceptar',
                        confirmButtonColor: '#dd9755',
                        background: 'rgb(43, 43, 43)',
                        color: '#ffffff'
                    });
                } else {
                    alert("Tu carrito está vacío.");
                }
                return;
            }

            if (typeof Swal !== 'undefined') {
                Swal.fire({
                    title: 'Procesando pago...',
                    text: `Pagando un total de ${cartTotalPrice.textContent}. ¡Esta es una simulación!`,
                    icon: 'success',
                    confirmButtonText: 'Aceptar',
                    confirmButtonColor: '#dd9755',
                    background: 'rgb(43, 43, 43)',
                    color: '#ffffff'
                }).then(() => {
                    cart = []; // Vacía el carrito
                    updateCartUI();
                    toggleCartModal(); // Cierra el modal
                });
            } else {
                alert(`Simulación de pago completada por ${cartTotalPrice.textContent}`);
                cart = [];
                updateCartUI();
                toggleCartModal();
            }
        });
    }
});