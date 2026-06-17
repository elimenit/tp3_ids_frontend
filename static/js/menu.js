// --- Helpers ---
function formatPrice(price) {
    return Number(price).toLocaleString('es-AR', {
        style: 'currency',
        currency: 'ARS',
        minimumFractionDigits: 0,
    });
}

// --- Estado Global del Carrito ---
let cart = [];

// --- Init y Lógica de Eventos ---
document.addEventListener('DOMContentLoaded', () => {
    
    // ==========================================
    // 1. LÓGICA DE PESTAÑAS (TABS) Y FILTRADO
    // ==========================================
    const menuTabs = document.getElementById('menu-tabs');
    
    if (menuTabs) {
        menuTabs.addEventListener('click', (e) => {
            const btn = e.target.closest('.tab-btn');
            if (!btn) return;
           
            // Cambiar clase activa
            document.querySelectorAll('.tab-btn').forEach(b => {
                b.classList.remove('active');
                b.setAttribute('aria-selected', 'false');
            });
            btn.classList.add('active');
            btn.setAttribute('aria-selected', 'true');
        
            // Filtrar las tarjetas
            const category = btn.dataset.category;
            document.querySelectorAll('.dish-card').forEach(card => {
                if (category === 'all' || card.dataset.category === category) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
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
    const menuGrid = document.getElementById('menu-grid');

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

    // Agregar al carrito (escuchando el grid)
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
                
                // Feedback visual
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

    // Eliminar del carrito
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
                    cart = [];
                    updateCartUI();
                    toggleCartModal();
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
//Cuenta los repetidos en el carrito
function buildDeliveryPayload() {
    const quantities = {};

    cart.forEach(item => {
        const id = Number(item.id);

        if (!quantities[id]) {
            quantities[id] = 0;
        }

        quantities[id]++;
    });

    return {
        list_menus: Object.entries(quantities).map(
            ([id, quantity]) => [Number(id), quantity]
        ),
        address: "direccion_usuario",
        date: new Date().toISOString()
    };
}

const deliveryBtn = document.getElementById("btn-delivery");

deliveryBtn?.addEventListener("click", async (e) => {
    e.preventDefault();

    if (cart.length === 0) {
        Swal.fire({
            title: 'Carrito vacío',
            text: 'Agrega algunos platos antes de solicitar un delivery.',
            icon: 'warning',
            confirmButtonColor: '#dd9755',
            background: 'rgb(43, 43, 43)',
            color: '#ffffff'
        });
        return;
    }

    // Agrupar productos repetidos
    const groupedMenus = {};

    cart.forEach(item => {
        const id = Number(item.id);

        if (!groupedMenus[id]) {
            groupedMenus[id] = 0;
        }

        groupedMenus[id] += 1;
    });

    const deliveryData = {
        list_menus: Object.entries(groupedMenus).map(
            ([id, quantity]) => [Number(id), quantity]
        ),
        address: "direccion_usuario",
        date: new Date().toISOString()
    };

    try {
        const response = await fetch("/deliveries", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(deliveryData)
        });

        // 👇 leer SOLO UNA VEZ como texto primero
        const text = await response.text();

        let data;
        try {
            data = JSON.parse(text);
        } catch (e) {
            throw new Error("Respuesta del servidor no es JSON válido");
        }

        if (!response.ok) {
            throw new Error(data.message || "Error al crear delivery");
        }

        Swal.fire({
            title: 'Delivery creado',
            text: data.message || 'Tu pedido fue enviado correctamente.',
            icon: 'success',
            confirmButtonColor: '#dd9755',
            background: 'rgb(43, 43, 43)',
            color: '#ffffff'
        }).then(() => {
            cart = [];
            updateCartUI();
            toggleCartModal();
            window.location.href = "/deliveries";
        });

    } catch (error) {
        console.error(error);

        Swal.fire({
            title: 'Error',
            text: error.message,
            icon: 'error'
        });
    }
});