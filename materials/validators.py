from rest_framework import serializers
from urllib.parse import urlparse
import re


def validate_youtube_url(value):
    """
    Функция-валидатор для проверки YouTube ссылок
    """
    if not value:
        return None

    parsed = urlparse(value)
    allowed_domains = ('youtube.com', 'youtu.be')

    # Проверка домена
    if not any(parsed.netloc.endswith(domain) for domain in allowed_domains):
        raise serializers.ValidationError(
            'Допустимы только ссылки на YouTube (youtube.com или youtu.be)'
        )

    # Проверка формата ссылки
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )

    if not re.match(youtube_regex, value):
        raise serializers.ValidationError('Неверный формат YouTube ссылки')
