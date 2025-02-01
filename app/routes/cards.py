from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.card import Card, UserCard

cards_bp = Blueprint('cards', __name__)


@cards_bp.route('/get_cards', methods=['GET'])
@jwt_required()
def get_cards():
    user_id = get_jwt_identity()
    user_cards = UserCard.query.filter_by(user_id=user_id).all()
    cards_data = []
    for user_card in user_cards:
        card = Card.query.get(user_card.card_id)
        if card:
            cards_data.append({
                'id': card.id,
                'name': card.name,
                'job': card.job,
                'company_name': card.company_name,
                'phones': card.phones,
                'email': card.email,
                'address': card.address,
                'websites': card.websites,
                'social_medias': card.social_medias,
                'competencies': card.competencies,
                'talk_info': card.talk_info
            })
    return jsonify(cards_data), 200


@cards_bp.route('/add_card', methods=['POST'])
@jwt_required()
def add_card():
    data = request.get_json()

    name = data.get('name')
    job = data.get('job')
    company_name = data.get('company_name')
    phones = data.get('phones', [])
    email = data.get('email', [])
    address = data.get('address')
    websites = data.get('websites', [])
    social_medias = data.get('social_medias', [])
    competencies = data.get('competencies')
    talk_info = data.get('talk_info', [])
    user_id = get_jwt_identity()

    new_card = Card(
        name=name,
        job=job,
        company_name=company_name,
        phones=phones,
        email=email,
        address=address,
        websites=websites,
        social_medias=social_medias,
        competencies=competencies,
        talk_info=talk_info
    )

    db.session.add(new_card)
    db.session.commit()

    user_card = UserCard(user_id=user_id, card_id=new_card.id)
    db.session.add(user_card)
    db.session.commit()

    return jsonify({'msg': 'Pack added successfully'}), 201
