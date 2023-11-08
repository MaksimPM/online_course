import re
from rest_framework.serializers import ValidationError

YOUTUBE_URL = 'https://www.youtube.com'


class DescriptionValidator:
    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        """Если в описании присутствует любой url кроме Youtube, то вызывает ошибку валидации"""

        pattern = 'https://'
        if 'description' in value:
            urls_in_description = re.findall(pattern, value['description'])
            youtube_urls_in_description = re.findall(YOUTUBE_URL, value['description'])
            if len(urls_in_description) != 0:
                if len(urls_in_description) != len(youtube_urls_in_description):
                    raise ValidationError('В описании указан недопустимый URL!')


class VideoUrlValidator:
    """Если в video_url указан любой url кроме Youtube, то вызывает ошибку валидации"""

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        if 'video_link' in value:
            if not YOUTUBE_URL in value['video_link']:
                raise ValidationError('Неверный YouTube URL-адрес!')
