import base64
import logging
import time
from io import BytesIO

import boto3
from PIL import Image
from botocore.exceptions import ClientError
from celery import Task
from django.conf import settings
from django.shortcuts import get_object_or_404

from apps.product.models import Product
from config.celery import celery_app

logger = logging.getLogger(__name__)


class ImageUploadTask(Task):
    name = "apps.product.tasks.image_upload_task"

    def run(self, product_uuid: str, data: dict) -> None:
        product = get_object_or_404(Product, uuid=product_uuid)
        file = data.get("file")
        filename = data.get("name")
        mimetype = data.get("mimetype")
        image_bytes = base64.b64decode(file)

        # rotate the image
        st = time.time()
        rotated_image_file = self.perform_image_rotation(image_bytes, mimetype)
        rotate_duration = time.time() - st

        # save product model
        product.logo = self.save_file_to_s3(rotated_image_file, filename)
        product.rotate_duration = rotate_duration
        product.save()

    def perform_image_rotation(self, image_bytes: bytes, mimetype: str) -> bytes:
        img = Image.open(BytesIO(image_bytes))
        rotated_img = img.rotate(180)
        format_str = mimetype.split("/")[1].upper()

        with BytesIO() as buffer:
            rotated_img.save(buffer, format=format_str)
            image_bytes = buffer.getvalue()

        return image_bytes

    def save_file_to_s3(self, file: bytes, filename: str) -> str:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        filepath = f"{settings.PUBLIC_MEDIA_LOCATION}/{filename}"
        try:
            s3_client.upload_fileobj(
                Fileobj=BytesIO(file), Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=filepath
            )
        except ClientError as e:
            logger.error(e)
            raise Exception("Error uploading file to S3")

        s3_url = f"{settings.MEDIA_URL}{filename}"
        logger.info(f"File uploaded to S3: {s3_url}")
        return s3_url


celery_app.tasks.register(ImageUploadTask())
