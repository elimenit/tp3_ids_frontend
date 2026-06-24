from services.public.reviews import get_reviews, get_my_reservations, create_review, update_review, delete_review
from utils.helpers import flash_message
from services.public.users import get_current_user
from flask import Blueprint, render_template, request, redirect, url_for

public_bp_reviews = Blueprint('public_reviews', __name__)


@public_bp_reviews.route("/", methods=["GET"])
def show():
    user = get_current_user()
    token = request.cookies.get('session_token')

    reviews = get_reviews() or []

    reservations = []
    if token:
        result, status = get_my_reservations(token)
        if result:
            reservations = [r for r in result if r.get('status_reservation') == 'Arrived']

    return render_template('public/reviews/reviews.html',
        user=user,
        reviews=reviews,
        reservations=reservations,
    )


@public_bp_reviews.post("/create")
def create():
    token = request.cookies.get('session_token')
    if not token:
        return redirect(url_for('public_auth.login'))

    data = {
        'reservation_id': request.form.get('reservation_id'),
        'description': request.form.get('description'),
        'stars': request.form.get('stars'),
    }
    success, response, status = create_review(token, data)

    if success:
        flash_message('Reseña publicada correctamente', category='success')
    else:
        flash_message(
            response.get('message', 'Error'),
            response.get('description', 'No se pudo publicar la reseña'),
            'error')

    return redirect(url_for('public_reviews.show'))


@public_bp_reviews.post("/update/<int:review_id>")
def update(review_id: int):
    token = request.cookies.get('session_token')
    if not token:
        return redirect(url_for('public_auth.login'))

    data = {
        'description': request.form.get('description'),
        'stars': request.form.get('stars'),
    }
    success, response, status = update_review(token, review_id, data)

    if success:
        flash_message('Reseña actualizada correctamente', category='success')
    else:
        flash_message(
            response.get('message', 'Error'),
            response.get('description', 'No se pudo actualizar la reseña'),
            'error')

    return redirect(url_for('public_reviews.show'))


@public_bp_reviews.post("/delete/<int:review_id>")
def remove(review_id: int):
    token = request.cookies.get('session_token')
    if not token:
        return redirect(url_for('public_auth.login'))

    success, response, status = delete_review(token, review_id)

    if success:
        flash_message('Reseña eliminada correctamente', category='success')
    else:
        flash_message(
            response.get('message', 'Error'),
            response.get('description', 'No se pudo eliminar la reseña'),
            'error')

    return redirect(url_for('public_reviews.show'))
