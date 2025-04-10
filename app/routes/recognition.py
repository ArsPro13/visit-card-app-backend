from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services.recognition import get_mocked_summary, get_mocked_vcard, extract_summary, extract_vcard_from_image

recognition_bp = Blueprint('recognition', __name__)


@recognition_bp.route('/recognize_image', methods=['POST'])
@jwt_required()
def recognize_image():
    data = request.get_json()
    image = data.get('image')

    try:
        card = extract_vcard_from_image(image)
    except Exception:
        return {}, 500

    return jsonify(card), 200


@recognition_bp.route('/recognize_speech', methods=['POST'])
@jwt_required()
def recognize_speech():
    data = request.get_json()
    speech_text = data.get('speech_text')

    try:
        speech_summary = extract_summary(speech_text)
    except Exception:
        return {}, 500

    return jsonify(speech_summary), 200
