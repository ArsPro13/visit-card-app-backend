import random

from app.mock.mocked_card import *


def process_recognizing_image(image):
    random_number = random.randint(0, 10)

    return {
        'name': mocked_cards[random_number]["name"],
        'job': mocked_cards[random_number]["job"],
        'companyName': mocked_cards[random_number]["company_name"],
        'phones': mocked_cards[random_number]["phones"],
        'email': mocked_cards[random_number]["email"],
        'address': mocked_cards[random_number]["address"],
        'websites': mocked_cards[random_number]["websites"],
        'socialMedias': mocked_cards[random_number]["social_medias"],
        'competencies': mocked_cards[random_number]["competencies"],
    }


def process_recognizing_speech(speech_text):
    random_number = random.randint(0, 10)

    return {
        'speech_info': f'Обсудили {speech_topics[random_number]}'
    }
