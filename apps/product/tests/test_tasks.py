import base64
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.product.models import Product
from apps.product.tasks import ImageUploadTask


class ImageUploadTaskTestCase(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product', description='This is a test product'
        )
        self.file = SimpleUploadedFile(
            name='test_image.png', content=b'random_data', content_type='image/png'
        )
        self.data = {
            'name': self.file.name,
            'mimetype': self.file.content_type,
            'file': self.get_base64_encoded_file_content(self.file)
        }

    def tearDown(self):
        self.product.delete()

    def get_base64_encoded_file_content(self, file):
        with file.open(mode='rb') as f:
            encoded_content = base64.b64encode(f.read())
        return encoded_content.decode('utf-8')

    @patch.object(ImageUploadTask, 'perform_image_rotation')
    @patch.object(ImageUploadTask, 'save_file_to_s3')
    def test_image_upload_task(self, mock_save_file_to_s3, mock_perform_image_rotation):
        mock_perform_image_rotation.return_value = b'rotated_image_content'
        mock_save_file_to_s3.return_value = 'https://test-media-url/test_image.png'

        ImageUploadTask().run(self.product.uuid, self.data)

        self.product.refresh_from_db()
        self.assertEqual(self.product.logo, 'https://test-media-url/test_image.png')
        mock_save_file_to_s3.assert_called_once_with(b'rotated_image_content', 'test_image.png')
        mock_perform_image_rotation.assert_called_once_with(b'random_data', 'image/png')