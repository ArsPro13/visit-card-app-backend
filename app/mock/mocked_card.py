import random

speech_topics = [
    "новые подходы в AI",
    "безопасность облачных сервисов",
    "будущее мобильной разработки",
    "перспективы блокчейн-технологий",
    "развитие кибербезопасности",
    "влияние больших данных на бизнес",
    "новые тренды в DevOps",
    "применение машинного обучения в медицине",
    "автоматизация процессов в IT",
    "роль открытого ПО в корпоративной среде"
]

mocked_cards = [
    {
        'name': f'Person {i}',
        'job': ['mobile developer', 'backend developer', 'data scientist', 'AI engineer', 'security specialist'][i % 5],
        'company_name': f'Company {chr(65 + i)}',
        'phones': [f'89{i}1234567', f'76{i}7654321'],
        'email': [f'user{i}@example.com', f'contact{i}@business.org'],
        'address': [f'Street {i}, District {i % 3 + 1}', f'City {chr(65 + (i % 5))}'],
        'websites': [f'https://business{i}.com', f'https://portfolio{i}.dev'],
        'social_medias': [f'https://linkedin.com/in/person{i}', f'https://twitter.com/user{i}'],
        'competencies': ['mobile development', 'cloud computing', 'AI research', 'network security', 'software architecture'][i % 5:],
        'speech_info': f'Обсудили {speech_topics[i]} и их влияние на индустрию.'
    } for i in range(10)
]