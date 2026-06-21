import { showAlert } from '../general/alerts.js';

const PAGE_LIMIT = 10;

let currentUserId = null;
let reviewsCache = [];
let editingReviewId = null;
let selectedStars = 0;
let currentOffset = 0;
let hasMore = true;

// --- Elementos del DOM ---

let formSection, formLoading, formNoReservations, reviewForm, reservationWrapper;
let fieldReservation, fieldStars, fieldDescription, formError;
let btnSubmit, btnCancelEdit;
let reviewsLoading, reviewsError, reviewsList, btnLoadMore;


// --- Helpers de UI ---

function showFormError(msg) {
    formError.textContent = msg;
    formError.hidden = false;
}

function clearFormError() {
    formError.hidden = true;
    formError.textContent = '';
}

function setStars(value) {
    selectedStars = value;
    fieldStars.value = value;
    document.querySelectorAll('.star-btn').forEach(btn => {
        btn.classList.toggle('active', Number(btn.dataset.value) <= value);
    });
}

function resetForm() {
    reviewForm.reset();
    editingReviewId = null;
    reviewForm.querySelector('#review-id').value = '';
    setStars(0);
    clearFormError();
    btnCancelEdit.hidden = true;
    btnSubmit.textContent = 'Publicar reseña';

    if (reservationWrapper) reservationWrapper.hidden = false;

    // Si no había reservas Arrived, volver a mostrar el mensaje y ocultar el form
    const hasArrivedOptions = fieldReservation && fieldReservation.options.length > 1;
    if (!hasArrivedOptions) {
        reviewForm.hidden = true;
        formNoReservations.hidden = false;
    }
}

function formatDate(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    if (isNaN(date)) return dateStr;
    return date.toLocaleDateString('es-AR', { day: '2-digit', month: 'short', year: 'numeric' });
}

function starsHtml(count) {
    return '★'.repeat(count) + '☆'.repeat(5 - count);
}


// --- Cargar reservas para el selector ---

async function loadReservations() {
    try {
        const res = await fetch('/reviews/reservations');
        if (res.status === 401) {
            formLoading.hidden = true;
            return;
        }
        if (!res.ok) throw new Error();

        const reservations = await res.json();
        
        const arrived = reservations.filter(r => r.status_reservation === 'Arrived');

        formLoading.hidden = true;

        if (arrived.length === 0) {
            formNoReservations.hidden = false;
            return;
        }

        arrived.forEach(r => {
            const option = document.createElement('option');
            option.value = r.id;
            option.textContent = `Reserva #${r.id} — ${formatDate(r.reservation_datetime)}`;
            fieldReservation.appendChild(option);
        });

        reviewForm.hidden = false;
    } catch {
        formLoading.hidden = true;
        formNoReservations.hidden = false;
    }
}


// --- Cargar y renderizar reseñas ---

async function loadReviews(reset = false) {
    if (reset) {
        currentOffset = 0;
        hasMore = true;
        reviewsCache = [];
        reviewsList.innerHTML = '';
    }

    reviewsLoading.hidden = false;
    reviewsError.hidden = true;
    btnLoadMore.hidden = true;

    try {
        const res = await fetch(`/reviews/all?_limit=${PAGE_LIMIT}&_offset=${currentOffset}`);
        if (!res.ok) throw new Error();
        const page = await res.json();

        reviewsCache = reviewsCache.concat(page);
        appendReviews(page);

        hasMore = page.length === PAGE_LIMIT;
        currentOffset += page.length;
        btnLoadMore.hidden = !hasMore;
    } catch {
        reviewsError.textContent = 'No se pudieron cargar las reseñas. Verificá que el servidor esté activo.';
        reviewsError.hidden = false;
    } finally {
        reviewsLoading.hidden = true;
        reviewsList.hidden = false;
    }
}

function appendReviews(reviews) {
    if (reviewsCache.length === 0) {
        reviewsList.innerHTML = '<p class="empty-message">Todavía no hay reseñas. ¡Sé el primero!</p>';
        return;
    }

    reviews.forEach(r => reviewsList.appendChild(renderCard(r)));
}

function renderCard(review) {
    const article = document.createElement('article');
    article.className = 'review-card';
    article.dataset.id = review.id;

    const isOwner = currentUserId && review.user_id === currentUserId;

    article.innerHTML = `
        <div class="review-card-header">
            <div class="review-meta">
                <span class="review-author">${review.user_name}</span>
                <span class="review-date">${formatDate(review.created_at)}</span>
            </div>
            <span class="review-stars">${starsHtml(review.stars)}</span>
        </div>
        <p class="review-comment">${review.description}</p>
        ${isOwner ? `
        <div class="review-actions">
            <button class="btn-icon btn-edit" data-action="edit" data-id="${review.id}">Editar</button>
            <button class="btn-icon btn-danger" data-action="delete" data-id="${review.id}">Eliminar</button>
        </div>` : ''}
    `;
    return article;
}


// --- Obtener usuario actual ---

async function fetchCurrentUser() {
    try {
        const res = await fetch('/users/me');
        if (res.ok) {
            const user = await res.json();
            currentUserId = user.id;
        }
    } catch {
        // sin sesión activa
    }
}


// --- CRUD ---

async function submitReview(e) {
    e.preventDefault();
    clearFormError();

    const isEdit = Boolean(editingReviewId);
    const stars = Number(fieldStars.value);
    const description = fieldDescription.value.trim();

    if (stars < 1 || stars > 5) {
        showFormError('Seleccioná entre 1 y 5 estrellas.');
        return;
    }
    if (!description) {
        showFormError('El comentario no puede estar vacío.');
        return;
    }

    const payload = { description, stars };
    if (!isEdit) {
        const reservationId = Number(fieldReservation.value);
        if (!reservationId) {
            showFormError('Seleccioná una reserva.');
            return;
        }
        payload.reservation_id = reservationId;
    }

    btnSubmit.disabled = true;
    btnSubmit.textContent = 'Guardando...';

    try {
        const url = isEdit ? `/reviews/${editingReviewId}` : '/reviews/create';
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

        resetForm();
        showAlert('Listo', isEdit ? 'Reseña actualizada correctamente.' : 'Reseña publicada correctamente.', 'success');
        await loadReviews(true);
    } catch (err) {
        showFormError(err.message || 'Ocurrió un error al guardar la reseña.');
    } finally {
        btnSubmit.disabled = false;
        btnSubmit.textContent = isEdit ? 'Guardar cambios' : 'Publicar reseña';
    }
}

function startEdit(reviewId) {
    const review = reviewsCache.find(r => r.id === reviewId);
    if (!review) return;

    editingReviewId = reviewId;
    reviewForm.querySelector('#review-id').value = reviewId;
    fieldDescription.value = review.description;
    setStars(review.stars);
    clearFormError();
    btnCancelEdit.hidden = false;
    btnSubmit.textContent = 'Guardar cambios';

    if (reservationWrapper) reservationWrapper.hidden = true;

    // Mostrar el formulario aunque no tenga reservas Arrived
    formNoReservations.hidden = true;
    reviewForm.hidden = false;

    formSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function deleteReview(reviewId) {
    const review = reviewsCache.find(r => r.id === reviewId);
    if (!review) return;

    const result = await showAlert(
        '¿Eliminar reseña?',
        'Esta acción no se puede deshacer.',
        'warning'
    );
    if (!result.isConfirmed) return;

    try {
        const res = await fetch(`/reviews/${reviewId}`, { method: 'DELETE' });
        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            throw new Error(data.description || data.mensaje || `HTTP ${res.status}`);
        }
        await loadReviews(true);
    } catch (err) {
        reviewsError.textContent = `No se pudo eliminar la reseña: ${err.message}`;
        reviewsError.hidden = false;
    }
}


// --- Init ---

async function init() {
    formSection = document.getElementById('form-section');
    formLoading = document.getElementById('form-loading');
    formNoReservations = document.getElementById('form-no-reservations');
    reviewForm = document.getElementById('review-form');
    reservationWrapper = document.getElementById('reservation-wrapper');
    fieldReservation = document.getElementById('field-reservation');
    fieldStars = document.getElementById('field-stars');
    fieldDescription = document.getElementById('field-description');
    formError = document.getElementById('form-error');
    btnSubmit = document.getElementById('btn-submit');
    btnCancelEdit = document.getElementById('btn-cancel-edit');
    reviewsLoading = document.getElementById('reviews-loading');
    reviewsError = document.getElementById('reviews-error');
    reviewsList = document.getElementById('reviews-list');
    btnLoadMore = document.getElementById('btn-load-more');

    // Estrellas interactivas
    document.querySelectorAll('.star-btn').forEach(btn => {
        btn.addEventListener('click', () => setStars(Number(btn.dataset.value)));
        btn.addEventListener('mouseenter', () => {
            document.querySelectorAll('.star-btn').forEach(b => {
                b.classList.toggle('active', Number(b.dataset.value) <= Number(btn.dataset.value));
            });
        });
        btn.addEventListener('mouseleave', () => setStars(selectedStars));
    });

    if (reviewForm) {
        reviewForm.addEventListener('submit', submitReview);
        btnCancelEdit.addEventListener('click', resetForm);
    }

    reviewsList.addEventListener('click', e => {
        const btn = e.target.closest('button[data-action]');
        if (!btn) return;
        const id = Number(btn.dataset.id);
        if (btn.dataset.action === 'edit') startEdit(id);
        else if (btn.dataset.action === 'delete') deleteReview(id);
    });

    await fetchCurrentUser();

    btnLoadMore.addEventListener('click', () => loadReviews());

    if (formSection) loadReservations();
    loadReviews(true);
}

document.addEventListener('DOMContentLoaded', init);
