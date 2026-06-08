const CATEGORY_LABELS = {
    burgers: 'Hamburguesas',
    drinks: 'Bebidas',
    pasta: 'Pastas',
    soup: 'Sopas',
};

let grid, loadingEl, errorEl;

function showLoading() {
    loadingEl.hidden = false;
    grid.hidden = true;
    errorEl.hidden = true;
}

function hideLoading() {
    loadingEl.hidden = true;
}

function showError(msg) {
    errorEl.textContent = msg;
    errorEl.hidden = false;
}

function renderCard(dish) {
    const article = document.createElement('article');
    article.className = 'dish-card';

    const imageHtml = dish.image_url
        ? `<img src="${dish.image_url}" alt="${dish.name}" loading="lazy">`
        : `<div class="dish-img-placeholder">🍽</div>`;

    const price = Number(dish.price).toLocaleString('es-AR', {
        style: 'currency',
        currency: 'ARS',
        minimumFractionDigits: 0,
    });

    article.innerHTML = `
        ${imageHtml}
        <div class="dish-card-body">
            <h2 class="dish-name">${dish.name}</h2>
            <p class="dish-description">${dish.description || ''}</p>
            <span class="dish-price">${price}</span>
        </div>
    `;
    return article;
}

function renderCards(dishes) {
    grid.innerHTML = '';

    if (dishes.length === 0) {
        grid.innerHTML = '<p class="empty-message">No hay platos en esta categoría.</p>';
    } else {
        dishes.forEach(dish => grid.appendChild(renderCard(dish)));
    }

    grid.hidden = false;
}

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

function setActiveTab(clickedBtn) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        btn.setAttribute('aria-selected', 'false');
    });
    clickedBtn.classList.add('active');
    clickedBtn.setAttribute('aria-selected', 'true');
}

function init() {
    grid = document.getElementById('menu-grid');
    loadingEl = document.getElementById('menu-loading');
    errorEl = document.getElementById('menu-error');

    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            setActiveTab(btn);
            fetchDishes(btn.dataset.category);
        });
    });

    fetchDishes('all');
}

document.addEventListener('DOMContentLoaded', init);
