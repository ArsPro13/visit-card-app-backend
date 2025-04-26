from gigachat import GigaChat
import json

from key import API_KEY
from openai import OpenAI

def extract_clean_json(text: str) -> str:
    """
    Удаляет лишние символы до первого '{' и после последнего '}'.
    Возвращает чистую JSON-строку.
    """
    start = text.find('{')
    end = text.rfind('}')
    if start == -1 or end == -1 or start > end:
        return ""  # Некорректный JSON
    return text[start:end + 1]


def normalize_result(data: dict) -> dict:
    fields = {
        'name': str,
        'surname': str,
        'job': str,
        'companyName': str,
        'phones': list,
        'email': list,
        'address': str,
        'websites': list,
        'socialMedias': list,
        'competencies': list
    }

    normalized = {}
    for key, expected_type in fields.items():
        value = data.get(key, [] if expected_type is list else "")
        if expected_type is list:
            if isinstance(value, str):
                normalized[key] = [value]
            elif isinstance(value, list):
                normalized[key] = value
            else:
                normalized[key] = []
        elif expected_type is str and isinstance(value, str):
            normalized[key] = value
        else:
            normalized[key] = ""
    return normalized


def extract_vcard_from_image(data_uri: str) -> dict:
    client = OpenAI(api_key="")

    if not data_uri.startswith('data:image/jpeg;base64,'):
        data_uri = f"data:image/jpeg;base64,{data_uri}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Извлеки данные с визитной карточки.\n"
                                "Верни ТОЛЬКО JSON БЕЗ КОММЕНТАРИЕВ, без описания и текста — только сам объект JSON со следующими полями:\n"
                                "name, surname, job, companyName, phones, email, address, websites, socialMedias, competencies.\n"
                                "Строки — как строки, списки — как массивы. Если данных нет — оставь пустыми.\n"
                                "Пример:\n"
                                "{ \"name\": \"Имя\", \"surname\": \"Фамилия\", ... }\n"
                                "Поле email должно быть массивом даже при одном адресе."
                            )
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": data_uri,
                                "detail": "auto"
                            }
                        }
                    ]
                }
            ],
            max_tokens=700,
            temperature=0.3
        )

        print("Использованные токены: запрос - ", response.usage.prompt_tokens, ", ответ - ",
              response.usage.completion_tokens, sep="")

        content = response.choices[0].message.content.strip()
        return normalize_result(json.loads(extract_clean_json(content)))

    except Exception as e:
        print("Ошибка при извлечении данных с изображения:", e)
        return {
            'name': "",
            'surname': "",
            'job': "",
            'companyName': "",
            'phones': [],
            'email': [],
            'address': "",
            'websites': [],
            'socialMedias': [],
            'competencies': []
        }

def extract_summary(text):
    prompt = (
        f"Текст общения: \"{text}\"\n\n"
        "Извлеки ключевые факты из текста. Каждый пункт должен быть формулирован как отдельное, связное и понятное предложение, "
        "которое можно читать независимо от остального контекста. Сохраняй конкретику (имена, цифры, договорённости, действия). НЕ ДОДУМЫВАЙ ФАКТЫ\n"
        "Если есть личные детали (например, хобби, семейное положение) — включи как отдельный пункт.\n"
        "Ответ верни строго в формате JSON-массива строк. Пример:\n"
        "[\"Обсуждались поставки стали на заводы по сниженной цене\", \"Собеседник — специалист, увлекается хоккеем\"]\n"
        "Если невозможно извлечь ни одного факта — верни []"
    )

    retries = 0
    while retries < 2:
        try:
            with GigaChat(credentials=API_KEY, verify_ssl_certs=False) as giga:
                response = giga.chat(prompt)
                answer = response.choices[0].message.content.strip()
                print(response.choices[0], "")
                summary = json.loads(answer)

                if isinstance(summary, list) and all(isinstance(item, str) for item in summary):
                    return {'speech_info': summary}
        except (json.JSONDecodeError, Exception) as e:
            retries += 1

    return {'speech_info': []}



def get_mocked_vcard(data_uri: str) -> dict:
    return {
        'name': 'Иван',
        'surname': 'Иванов',
        'job': 'Программист',
        'companyName': 'TechCorp',
        'phones': ['+7 900 123 4567'],
        'email': ['ivan@example.com'],
        'address': 'ул. Пушкина, д. Колотушкина',
        'websites': ['https://ivan.tech'],
        'socialMedias': ['https://linkedin.com/in/ivanivanov'],
        'competencies': ['Python', 'AI']
    }


def get_mocked_summary(text) -> dict:
    return {
        'speech_info': [
            'Обсуждались условия сотрудничества с компанией TechCorp.',
            'Собеседник Иван увлекается ИИ и работает программистом.'
        ]
    }
