from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.product.forms import ProductForm
from apps.product.models import Product


class ProductFormTest(TestCase):

    def setUp(self):
        self.form_data = {
            "name": "Test Product",
            "description": "This is a test product",
        }
        self.logo_file = SimpleUploadedFile(
            "test_image.jpg",
            b"binary_content",
            content_type="image/jpeg"
        )

    def test_valid_form(self):
        form = ProductForm(data=self.form_data, files={"logo_file": self.logo_file})
        self.assertTrue(form.is_valid())
        product = form.save()
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "This is a test product")

    def test_invalid_form(self):
        form = ProductForm(data={}, files={"logo_file": self.logo_file})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn("name", form.errors)

    def test_invalid_logo_file_type(self):
        invalid_file = SimpleUploadedFile(
            "test_image.txt",
            b"binary_content",
            content_type="text/plain",
        )
        form = ProductForm(data=self.form_data, files={"logo_file": invalid_file})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn("logo_file", form.errors)
