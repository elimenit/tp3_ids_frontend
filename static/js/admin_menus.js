import { showAlert } from './alerts.js';

const CATEGORY_LABELS = {
    burgers: 'Hamburguesas',
    drinks: 'Bebidas',
    pasta: 'Pastas',
    soup: 'Sopas',
};

const dishCache = new Map();

let loadingEl, errorEl, tableEl, tbodyEl, modal, form, formError, modalTitle, labelAvailable;


// --- Helpers de UI ---

function showTableLoading() {
    loadingEl.hidden = false;
    tableEl.hidden = true;
    errorEl.hidden = true;
}

function hideTableLoading() {
    loadingEl.hidden = true;
}

function showTableError(msg) {
    errorEl.textContent = msg;
    errorEl.hidden = false;
}

function showFormError(msg) {
    formError.textContent = msg;
    formError.hidden = false;
}

function clearFormError() {
    formError.hidden = true;
    formError.textContent = '';
}

function openModal() {
    modal.hidden = false;
    document.getElementById('field-name').focus();
}

function closeModal() {
    modal.hidden = true;
    form.reset();
    document.getElementById('dish-id').value = '';
    clearFormError();
    labelAvailable.hidden = true;
}

function formatPrice(price) {
    return Number(price).toLocaleString('es-AR', {
        style: 'currency',
        currency: 'ARS',
        minimumFractionDigits: 0,
    });
}


// --- Carga y renderizado ---

async function loadDishes() {
    showTableLoading();
    dishCache.clear();

    try {
        const res = await fetch('/admin/menus/all');
        if (res.status === 401) {
            window.location.href = '/auth/login';
            return;
        }
        if (res.status === 403) {
            showTableError('No tenés permisos de administrador para acceder a este panel.');
            return;
        }
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const dishes = await res.json();
        dishes.forEach(d => dishCache.set(d.id, d));
        renderTable(dishes);
    } catch {
        showTableError('No se pudo cargar la lista de platos. Verificá que el servidor esté activo.');
    } finally {
        hideTableLoading();
    }
}

function renderTable(dishes) {
    tbodyEl.innerHTML = '';

    if (dishes.length === 0) {
        tbodyEl.innerHTML = '<tr><td colspan="6" class="table-empty">No hay platos cargados.</td></tr>';
    } else {
        dishes.forEach(dish => tbodyEl.appendChild(renderRow(dish)));
    }

    tableEl.hidden = false;
}

function renderRow(dish) {
    const tr = document.createElement('tr');

    const thumbHtml = dish.image_url
        ? `<img src="${dish.image_url}" alt="${dish.name}" class="dish-thumb">`
        : `<div class="dish-thumb-placeholder">🍽</div>`;

    const badgeHtml = dish.available
        ? `<span class="badge badge-available">Sí</span>`
        : `<span class="badge badge-unavailable">No</span>`;

    const toggleLabel = dish.available ? 'Desactivar' : 'Activar';
    const categoryLabel = CATEGORY_LABELS[dish.category] || dish.category;

    tr.innerHTML = `
        <td>${thumbHtml}</td>
        <td>${dish.name}</td>
        <td>${categoryLabel}</td>
        <td>${formatPrice(dish.price)}</td>
        <td>${badgeHtml}</td>
        <td>
            <div class="actions-cell">
                <button class="btn-icon btn-edit" data-action="edit" data-id="${dish.id}">Editar</button>
                <button class="btn-icon btn-toggle" data-action="toggle" data-id="${dish.id}">${toggleLabel}</button>
                <button class="btn-icon btn-danger" data-action="delete" data-id="${dish.id}">Eliminar</button>
            </div>
        </td>
    `;
    return tr;
}


// --- Modal: crear / editar ---

function openCreateModal() {
    modalTitle.textContent = 'Nuevo Plato';
    labelAvailable.hidden = true;
    openModal();
}

function openEditModal(dish) {
    modalTitle.textContent = 'Editar Plato';

    document.getElementById('dish-id').value = dish.id;
    document.getElementById('field-name').value = dish.name;
    document.getElementById('field-category').value = dish.category;
    document.getElementById('field-description').value = dish.description || '';
    document.getElementById('field-price').value = dish.price;
    document.getElementById('field-available').checked = dish.available;
    document.getElementById('field-image-url').value = dish.image_url || '';

    labelAvailable.hidden = false;
    openModal();
}

function buildPayload(isEdit) {
    const payload = {
        name: document.getElementById('field-name').value.trim(),
        category: document.getElementById('field-category').value,
        description: document.getElementById('field-description').value.trim(),
        price: parseFloat(document.getElementById('field-price').value),
        image_url: document.getElementById('field-image-url').value.trim() || null,
    };
    if (isEdit) {
        payload.available = document.getElementById('field-available').checked;
    }
    return payload;
}

function validatePayload(payload) {
    if (!payload.name) return 'El nombre es obligatorio.';
    if (!payload.category) return 'La categoría es obligatoria.';
    if (isNaN(payload.price) || payload.price <= 0) return 'El precio debe ser mayor a 0.';
    return null;
}


// --- CRUD ---

async function saveDish(e) {
    e.preventDefault();
    clearFormError();

    const dishId = document.getElementById('dish-id').value;
    const isEdit = Boolean(dishId);
    const payload = buildPayload(isEdit);

    const validationError = validatePayload(payload);
    if (validationError) {
        showFormError(validationError);
        return;
    }

    const btnSave = document.getElementById('btn-save');
    btnSave.disabled = true;
    btnSave.textContent = 'Guardando...';

    try {
        const url = isEdit ? `/admin/menus/${dishId}` : '/admin/menus/create';
        const method = isEdit ? 'PUT' : 'POST';

        const res = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            throw new Error(data.description || data.mensaje || `HTTP ${res.status}`);
        }

        closeModal();
        showAlert('Guardado', isEdit ? 'Plato actualizado correctamente.' : 'Plato creado correctamente.', 'success');
        await loadDishes();
    } catch (err) {
        showFormError(err.message || 'Ocurrió un error al guardar el plato.');
    } finally {
        btnSave.disabled = false;
        btnSave.textContent = 'Guardar';
    }
}

async function deleteDish(id) {
    const dish = dishCache.get(id);
    if (!dish) return;

    showAlert(`¿Eliminar "${dish.name}"?`, 'Esta acción no se puede deshacer.', 'warning').then(async (result) => {
        if (!result.isConfirmed) return;

        try {
            const res = await fetch(`/admin/menus/${id}`, { method: 'DELETE' });
            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                throw new Error(data.description || data.mensaje || `HTTP ${res.status}`);
            }
            await loadDishes();
        } catch (err) {
            showTableError(`No se pudo eliminar el plato: ${err.message}`);
        }
    });
}

async function toggleAvailable(dish) {
    const payload = {
        name: dish.name,
        category: dish.category,
        description: dish.description || '',
        price: dish.price,
        available: !dish.available,
        image_url: dish.image_url || null,
    };

    try {
        const res = await fetch(`/admin/menus/${dish.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            throw new Error(data.description || data.mensaje || `HTTP ${res.status}`);
        }
        await loadDishes();
    } catch (err) {
        showTableError(`No se pudo cambiar el estado: ${err.message}`);
    }
}


// --- Init ---

function init() {
    loadingEl = document.getElementById('admin-loading');
    errorEl = document.getElementById('admin-error');
    tableEl = document.getElementById('dishes-table');
    tbodyEl = document.getElementById('dishes-tbody');
    modal = document.getElementById('dish-modal');
    form = document.getElementById('dish-form');
    formError = document.getElementById('form-error');
    modalTitle = document.getElementById('modal-title');
    labelAvailable = document.getElementById('label-available');

    document.getElementById('btn-new-dish').addEventListener('click', openCreateModal);
    document.getElementById('btn-cancel').addEventListener('click', closeModal);
    form.addEventListener('submit', saveDish);

    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });

    tbodyEl.addEventListener('click', (e) => {
        const btn = e.target.closest('button[data-action]');
        if (!btn) return;

        const id = Number(btn.dataset.id);
        const dish = dishCache.get(id);
        if (!dish) return;

        const action = btn.dataset.action;
        if (action === 'edit') openEditModal(dish);
        else if (action === 'delete') deleteDish(id);
        else if (action === 'toggle') toggleAvailable(dish);
    });

    loadDishes();
}

document.addEventListener('DOMContentLoaded', init);
