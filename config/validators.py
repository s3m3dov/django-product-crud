from django.conf import settings
from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size
    limit = settings.MAX_FILE_UPLOAD_SIZE

    if filesize > limit:
        raise ValidationError(f"You cannot upload file more than {limit} bytes")
    else:
        return value


def validate_file_type(value):
    file_type = value.content_type
    if file_type not in settings.ALLOWED_FILE_TYPES:
        raise ValidationError(f"You cannot upload file of type {file_type}")
    else:
        return value
