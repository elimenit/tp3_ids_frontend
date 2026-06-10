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

// --- Init ---

document.addEventListener('DOMContentLoaded', async () => {
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
});
