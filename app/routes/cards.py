import time
import json

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import random
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
                'img': card.img or '',
                'name': card.name,
                'surname': card.surname,
                'job': card.job,
                'companyName': card.company_name,
                'phones': card.phones if card.phones else [],
                'email': card.email if card.email else [],
                'address': card.address,
                'websites': card.websites if card.websites else [],
                'socialMedias': card.social_medias if card.social_medias else [],
                'competencies': card.competencies.split(', ') if isinstance(card.competencies, str) else card.competencies,
                'talkInfo': card.talk_info if card.talk_info else []
            })
    return jsonify(cards_data), 200


@cards_bp.route('/add_card', methods=['POST'])
@jwt_required()
def add_card():
    data = request.get_json()

    name = data.get('name')
    surname = data.get('surname')
    job = data.get('job')
    company_name = data.get('companyName')
    phones = data.get('phones', [])
    email = data.get('email', [])
    address = data.get('address')
    websites = data.get('websites', [])
    social_medias = data.get('socialMedias', [])
    competencies = data.get('competencies', [])
    talk_info = data.get('talkInfo', [])
    img = data.get('img')

    user_id = get_jwt_identity()

    time.sleep(5)

    new_card = Card(
        name =name,
        surname=surname,
        job=job,
        company_name=company_name,
        phones=phones,
        email=email,
        address=address,
        websites=websites,
        social_medias=social_medias,
        competencies=', '.join(competencies) if isinstance(competencies, list) else competencies,
        talk_info=talk_info,
        img=img
    )

    db.session.add(new_card)
    db.session.commit()

    user_card = UserCard(user_id=user_id, card_id=new_card.id)
    db.session.add(user_card)
    db.session.commit()

    response_payload = {
        'id': new_card.id,
        'img': new_card.img or '',
        'name': new_card.name,
        'surname': new_card.surname,
        'job': new_card.job,
        'companyName': new_card.company_name,
        'phones': list(new_card.phones or []),
        'email': list(new_card.email or []),
        'address': new_card.address,
        'websites': list(new_card.websites or []),
        'socialMedias': list(new_card.social_medias or []),
        'competencies': new_card.competencies.split(', ') if isinstance(new_card.competencies, str) else list(
            new_card.competencies or []),
        'talkInfo': list(new_card.talk_info or [])
    }

    return jsonify(response_payload), 200


@cards_bp.route('/get_mocked_cards', methods=['GET'])
def get_mocked_cards():
    names = [
        ("Alice", "Johnson"), ("Bob", "Smith"), ("Charlie", "Brown"), ("David", "Lee"), ("Emma", "Wilson"),
        ("Sophia", "Martinez"), ("Ethan", "Walker"), ("Olivia", "Harris"), ("Liam", "Adams"), ("Ava", "Robinson"),
        ("Michael", "Thompson"), ("Isabella", "Scott"), ("James", "White"), ("Mia", "Carter"), ("Benjamin", "Hall"),
        ("Charlotte", "Green"), ("Daniel", "Wright"), ("Amelia", "Turner"), ("Matthew", "Lewis"), ("Harper", "Allen"),
        ("Joseph", "Young"), ("Evelyn", "King"), ("Samuel", "Hill"), ("Abigail", "Baker"), ("Henry", "Nelson"),
        ("Emily", "Perez"), ("Alexander", "Collins"), ("Scarlett", "Mitchell"), ("Lucas", "Roberts"), ("Grace", "Evans"),
        ("William", "Clark"), ("Victoria", "Edwards"), ("Jack", "Morris"), ("Lily", "Cooper"), ("Oliver", "Stewart"),
        ("Hannah", "Rivera"), ("Noah", "Sanchez"), ("Zoe", "Reed"), ("Jacob", "Bennett"), ("Madison", "Gray")
    ]
    jobs = [
        "Software Engineer", "Product Manager", "Data Scientist", "UX Designer", "Marketing Specialist",
        "DevOps Engineer", "Cybersecurity Analyst", "Business Analyst", "Financial Consultant", "HR Manager"
    ]

    companies = [
        "TechCorp", "InnoSoft", "DataWiz", "DesignPro", "MarketGenius",
        "CloudSync", "SecureNet", "BizSolutions", "FinancePros", "HRInnovate"
    ]

    addresses = [
        "123 Main St, NY", "456 Elm St, CA", "789 Oak St, TX", "321 Maple St, WA", "654 Pine St, FL",
        "987 Cedar St, IL", "852 Birch St, CO", "369 Spruce St, AZ", "741 Walnut St, GA", "258 Cherry St, MA"
    ]

    social_media_platforms = [
        "LinkedIn", "Twitter", "Facebook", "Instagram",
        "TikTok", "YouTube", "Snapchat", "Reddit", "Pinterest", "GitHub"
    ]

    time.sleep(7)

    def generate_mock_cards(n=5):
        visit_cards = []
        for i in range(1, n + 1):
            name, surname = random.choice(names)
            visit_card = {
                "id": i,
                "img": f"https://example.com/avatar{i}.png",
                "name": name,
                "surname": surname,
                "job": random.choice(jobs),
                "companyName": random.choice(companies),
                "phones": [f"+1-555-{random.randint(1000, 9999)}"],
                "email": [f"user{i}@example.com"],
                "address": random.choice(addresses),
                "websites": [f"https://example{i}.com"],
                "socialMedias": [random.choice(social_media_platforms)],
                "competencies": ["Python", "Swift", "JavaScript", "UI/UX", "Marketing"],
                "talkInfo": ["Agile Development", "AI & ML", "Business Strategy"]
            }
            visit_cards.append(visit_card)
        return visit_cards

    mock_data = generate_mock_cards(50)

    return jsonify(mock_data), 200
