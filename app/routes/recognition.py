from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services.recognition import extract_summary, extract_vcard_from_texts

recognition_bp = Blueprint('recognition', __name__)


@recognition_bp.route('/recognize_image', methods=['POST'])
@jwt_required()
def recognize_image():
    data = request.get_json()
    lines = data.get('lines')

    if not isinstance(lines, list) or not all(isinstance(line, str) for line in lines):
        return {"error": "Invalid input. 'lines' must be a list of strings."}, 400

    try:
        card = extract_vcard_from_texts(lines)
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
