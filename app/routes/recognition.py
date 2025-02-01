from flask import Blueprint, jsonify, request
from app.services.recognition import process_recognizing_image, process_recognizing_speech

recognition_bp = Blueprint('recognition', __name__)


@recognition_bp.route('/recognize_image', methods=['POST'])
def recognize_image():
    data = request.get_json()
    image = data.get('image')

    # todo: add deepseek api integration (unavailable right now)
    try:
        card = process_recognizing_image(image)
    except Exception:
        return {}, 500

    return jsonify(card), 200


@recognition_bp.route('/recognize_speech', methods=['POST'])
def recognize_speech():
    data = request.get_json()
    speech_text = data.get('speech_text')

    # todo: add deepseek api integration (unavailable right now)
    try:
        speech_summary = process_recognizing_speech(speech_text)
    except Exception:
        return {}, 500

    return jsonify(speech_summary), 200
