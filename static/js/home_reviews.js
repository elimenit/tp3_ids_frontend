function starsHtml(count) {
    return '★'.repeat(count) + '☆'.repeat(5 - count);
}

function formatDate(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    if (isNaN(date)) return dateStr;
    return date.toLocaleDateString('es-AR', { day: '2-digit', month: 'short', year: 'numeric' });
}

async function loadHomeReviews() {
    const carousel = document.getElementById('reviews-carousel');
    if (!carousel) return;

    try {
        const res = await fetch('/reviews/all?_limit=4&_offset=0');
        if (!res.ok) throw new Error();
        const latest = await res.json();

        if (latest.length === 0) {
            carousel.innerHTML = '<div class="review-card"><p class="review-comment">Todavía no hay reseñas.</p></div>';
            return;
        }

        carousel.innerHTML = latest.map(r => `
            <div class="review-card">
                <div class="review-stars">${starsHtml(r.stars)}</div>
                <p class="review-comment">${r.description}</p>
                <span class="review-author">— ${r.user_name} · ${formatDate(r.created_at)}</span>
            </div>
        `).join('');
    } catch {
        carousel.innerHTML = '<div class="review-card"><p class="review-comment">No se pudieron cargar las reseñas.</p></div>';
    }
}

document.addEventListener('DOMContentLoaded', loadHomeReviews);
