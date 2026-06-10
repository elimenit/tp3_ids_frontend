import { showAlert } from './alerts.js';

const dishCache = new Map();

// --- API ---

async function apiFetch(url, method = 'GET', body = null) {
    const options = { method, headers: {} };
    if (body) {
        options.headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(body);
    }
    const res = await fetch(url, options);
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.description || data.mensaje || `HTTP ${res.status}`);
    return data;
}

// --- Carga y renderizado ---

async function loadDishes() {
    document.getElementById('admin-loading').hidden = false;
    document.getElementById('dishes-table').hidden = true;
    dishCache.clear();

    try {
        const res = await fetch('/admin/menus/all');
        if (res.status === 401) { window.location.href = '/auth/login'; return; }
        if (res.status === 403) {
            showTableError('No tenés permisos de administrador para acceder a este panel.');
            return;
        }
        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const dishes = await res.json();
        dishes.forEach(d => dishCache.set(d.id, d));
        updateCategorySuggestions(dishes);
        renderTable(dishes);
    } catch {
        showTableError('No se pudo cargar la lista de platos. Verificá que el servidor esté activo.');
    } finally {
        document.getElementById('admin-loading').hidden = true;
    }
}

function showTableError(msg) {
    const el = document.getElementById('admin-error');
    el.textContent = msg;
    el.hidden = false;
}

function updateCategorySuggestions(dishes) {
    const unique = [...new Set(dishes.map(d => d.category))].sort();
    document.getElementById('category-suggestions').innerHTML = unique.map(c => `<option value="${c}">`).join('');
}

function renderTable(dishes) {
    const tbody = document.getElementById('dishes-tbody');

    if (dishes.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="table-empty">No hay platos cargados.</td></tr>';
    } else {
        tbody.innerHTML = '';
        dishes.forEach(dish => tbody.appendChild(renderRow(dish)));
    }

    document.getElementById('dishes-table').hidden = false;
}

function renderRow(dish) {
    const tr = document.createElement('tr');
    tr.innerHTML = `
        <td>${dish.image_url
            ? `<img src="${dish.image_url}" alt="" class="dish-thumb">`
            : `<div class="dish-thumb-placeholder">🍽</div>`}
        </td>
        <td>${dish.name}</td>
        <td>${dish.category}</td>
        <td>${formatPrice(dish.price)}</td>
        <td><span class="badge ${dish.available ? 'badge-available' : 'badge-unavailable'}">${dish.available ? 'Sí' : 'No'}</span></td>
        <td>
            <div class="actions-cell">
                <button class="btn-icon btn-edit"   data-action="edit"   data-id="${dish.id}">Editar</button>
                <button class="btn-icon btn-toggle" data-action="toggle" data-id="${dish.id}">${dish.available ? 'Desactivar' : 'Activar'}</button>
                <button class="btn-icon btn-danger" data-action="delete" data-id="${dish.id}">Eliminar</button>
            </div>
        </td>
    `;
    return tr;
}

function formatPrice(price) {
    return Number(price).toLocaleString('es-AR', {
        style: 'currency',
        currency: 'ARS',
        minimumFractionDigits: 0,
    });
}

// --- Modal ---

function openModal(title, showAvailable) {
    document.getElementById('modal-title').textContent = title;
    document.getElementById('label-available').hidden = !showAvailable;
    document.getElementById('dish-modal').hidden = false;
    document.getElementById('field-name').focus();
}

function closeModal() {
    document.getElementById('dish-modal').hidden = true;
    document.getElementById('dish-form').reset();
    document.getElementById('dish-id').value = '';
    setFormError('');
    document.getElementById('label-available').hidden = true;
}

function openCreateModal() {
    openModal('Nuevo Plato', false);
}

function openEditModal(dish) {
    document.getElementById('dish-id').value               = dish.id;
    document.getElementById('field-name').value            = dish.name;
    document.getElementById('field-category').value        = dish.category;
    document.getElementById('field-description').value     = dish.description || '';
    document.getElementById('field-price').value           = dish.price;
    document.getElementById('field-available').checked     = dish.available;
    document.getElementById('field-image-url').value       = dish.image_url || '';
    openModal('Editar Plato', true);
}

function setFormError(msg) {
    const el = document.getElementById('form-error');
    el.textContent = msg;
    el.hidden = !msg;
}

function buildPayload(isEdit) {
    const payload = {
        name:        document.getElementById('field-name').value.trim(),
        category:    document.getElementById('field-category').value.trim(),
        description: document.getElementById('field-description').value.trim(),
        price:       parseFloat(document.getElementById('field-price').value),
        image_url:   document.getElementById('field-image-url').value.trim() || null,
    };
    if (isEdit) payload.available = document.getElementById('field-available').checked;
    return payload;
}

function validatePayload({ name, category, price }) {
    if (!name)                      return 'El nombre es obligatorio.';
    if (!category)                  return 'La categoría es obligatoria.';
    if (isNaN(price) || price <= 0) return 'El precio debe ser mayor a 0.';
    return null;
}

// --- CRUD ---

async function saveDish(e) {
    e.preventDefault();
    setFormError('');

    const dishId = document.getElementById('dish-id').value;
    const isEdit = Boolean(dishId);
    const payload = buildPayload(isEdit);
    const error = validatePayload(payload);
    if (error) { setFormError(error); return; }

    const btnSave = document.getElementById('btn-save');
    btnSave.disabled = true;
    btnSave.textContent = 'Guardando...';

    try {
        const url    = isEdit ? `/admin/menus/${dishId}` : '/admin/menus/create';
        const method = isEdit ? 'PUT' : 'POST';
        await apiFetch(url, method, payload);
        closeModal();
        showAlert('Guardado', isEdit ? 'Plato actualizado.' : 'Plato creado.', 'success');
        await loadDishes();
    } catch (err) {
        setFormError(err.message || 'Ocurrió un error al guardar el plato.');
    } finally {
        btnSave.disabled = false;
        btnSave.textContent = 'Guardar';
    }
}

async function deleteDish(dish) {
    const result = await showAlert(`¿Eliminar "${dish.name}"?`, 'Esta acción no se puede deshacer.', 'warning');
    if (!result.isConfirmed) 
        return;

    try {
        await apiFetch(`/admin/menus/${dish.id}`, 'DELETE');
        await loadDishes();
    } catch (err) {
        showTableError(`No se pudo eliminar el plato: ${err.message}`);
    }
}

async function toggleAvailable(dish) {
    try {
        await apiFetch(`/admin/menus/${dish.id}`, 'PUT', {
            name:        dish.name,
            category:    dish.category,
            description: dish.description || '',
            price:       dish.price,
            available:   !dish.available,
            image_url:   dish.image_url || null,
        });
        await loadDishes();
    } catch (err) {
        showTableError(`No se pudo cambiar el estado: ${err.message}`);
    }
}

// --- Init ---

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('btn-new-dish').addEventListener('click', openCreateModal);
    document.getElementById('btn-cancel').addEventListener('click', closeModal);
    document.getElementById('dish-form').addEventListener('submit', saveDish);

    document.getElementById('dish-modal').addEventListener('click', e => {
        if (e.target === document.getElementById('dish-modal')) closeModal();
    });

    document.getElementById('dishes-tbody').addEventListener('click', e => {
        const btn = e.target.closest('button[data-action]');
        if (!btn) return;
        const dish = dishCache.get(Number(btn.dataset.id));
        if (!dish) return;
        if (btn.dataset.action === 'edit')   openEditModal(dish);
        if (btn.dataset.action === 'delete') deleteDish(dish);
        if (btn.dataset.action === 'toggle') toggleAvailable(dish);
    });

    loadDishes();
});
