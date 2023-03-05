from django.conf import settings
from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size
    limit = settings.MAX_FILE_UPLOAD_SIZE

    if filesize > limit:
        raise ValidationError(f"You cannot upload file more than {limit} bytes")
    else:
        return value
