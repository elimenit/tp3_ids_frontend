from services.public.reviews import get_reviews, get_my_reservations, create_review, update_review, delete_review
from services.public.users import get_current_user
from utils.helpers import flash_message

from flask import Blueprint, render_template, request, jsonify, url_for, redirect

public_bp_reviews = Blueprint('public_reviews', __name__)


@public_bp_reviews.route("/", methods=["GET"])
def show():
    user = get_current_user()
    return render_template('public/reviews/reviews.html',
        user=user
    )


@public_bp_reviews.route("/all", methods=["GET"])
def all_reviews():
    reviews = get_reviews()
    if reviews is None:
        flash_message("Error", "No se pudo obtener las reseñas")
        return redirect(url_for('main'))
    return jsonify(reviews)


@public_bp_reviews.route("/reservations", methods=["GET"])
def user_reservations():
    token = request.cookies.get('session_token')
    if not token:
        return jsonify({"mensaje": "No autorizado"}), 401
    reservations, status = get_my_reservations(token)
    if status == 401:
        return jsonify({"mensaje": "Sesión expirada"}), 401
    if reservations is None:
        flash_message("Error", "No se pudo obtener las reservas")
        return redirect(url_for('main'))
    return jsonify(reservations)


@public_bp_reviews.route("/create", methods=["POST"])
def create():
    token = request.cookies.get('session_token')
    if not token:
        return jsonify({"mensaje": "No autorizado"}), 401
    data = request.get_json()
    success, response, status = create_review(token, data)
    return jsonify(response), 201 if success else status


@public_bp_reviews.route("/<int:review_id>", methods=["PUT"])
def update(review_id: int):
    token = request.cookies.get('session_token')
    if not token:
        return jsonify({"mensaje": "No autorizado"}), 401
    data = request.get_json()
    success, response, status = update_review(token, review_id, data)
    return jsonify(response), 200 if success else status


@public_bp_reviews.route("/<int:review_id>", methods=["DELETE"])
def remove(review_id: int):
    token = request.cookies.get('session_token')
    if not token:
        return jsonify({"mensaje": "No autorizado"}), 401
    success, response, status = delete_review(token, review_id)
    return jsonify(response), 200 if success else status
