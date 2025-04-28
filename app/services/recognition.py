from gigachat import GigaChat
import json

from key import API_KEY

def extract_clean_json(text: str) -> str:
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


def extract_vcard_from_texts(lines: list[str]) -> dict:
    joined = "\n".join(lines)
    prompt = (
        "Ты — AI-помощник, извлекающий данные с визитной карточки из фрагментов текста.\n\n"
        "Даны следующие строки:\n"
        f"{joined}\n\n"
        "Классифицируй их и верни ТОЛЬКО JSON-объект без дополнительных комментариев, "
        "со следующими полями:\n"
        "name, surname, job, companyName, phones, email, address, websites, socialMedias, competencies.\n"
        "- Если имя и фамилия оказались в одной строке — разложи их по полям name и surname.\n"
        "- Строки — как строки, списки — как массивы.\n"
        "- Если для какого-то поля данных нет — используй пустую строку или пустой массив.\n\n"
        "Пример ответа:\n"
        "{\n"
        "  \"name\": \"Имя\",\n"
        "  \"surname\": \"Фамилия\",\n"
        "  \"job\": \"Должность\",\n"
        "  \"companyName\": \"Компания\",\n"
        "  \"phones\": [\"+7 (123) 456-78-90\"],\n"
        "  \"email\": [\"user@example.com\"],\n"
        "  \"address\": \"Улица, город, страна\",\n"
        "  \"websites\": [\"https://example.com\"],\n"
        "  \"socialMedias\": [\"https://linkedin.com/in/username\"],\n"
        "  \"competencies\": [\"Управление проектами\", \"Продажи\"]\n"
        "}"
    )

    retries = 0
    while retries < 2:
        try:
            with GigaChat(credentials=API_KEY, verify_ssl_certs=False) as giga:
                response = giga.chat(prompt)
                answer = response.choices[0].message.content.strip()
                data = json.loads(extract_clean_json(answer))
                return normalize_result(data)
        except (json.JSONDecodeError, Exception):
            retries += 1

    return {
        "name": "",
        "surname": "",
        "job": "",
        "companyName": "",
        "phones": [],
        "email": [],
        "address": "",
        "websites": [],
        "socialMedias": [],
        "competencies": []
    }

def extract_summary(text):
    prompt = (
        f"Текст общения: \"{text}\"\n\n"
        "Извлеки ключевые факты из текста. Каждый пункт должен быть сформулирован как отдельное, "
        "связанное и понятное предложение, которое можно читать независимо от контекста. Сохраняй "
        "конкретику (имена, цифры, договорённости, действия). Основывайся ТОЛЬКО на приведённом тексте — "
        "никакой дополнительной информации и фактов, которых нет в тексте, быть не должно.\n"
        "Если есть личные детали (например, хобби, семейное положение), включи их как отдельный пункт.\n"
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
