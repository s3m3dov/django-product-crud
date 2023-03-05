import uuid as uuid_lib

from django.test import TestCase
from django.utils import timezone

from apps.product.models import Product


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="This is a test product.",
            logo="https://example.com/test.png",
            rotate_duration=10.0,
            modified=True
        )

    def test_product_fields(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.description, "This is a test product.")
        self.assertTrue(isinstance(self.product.uuid, uuid_lib.UUID))
        self.assertTrue(self.product.created <= timezone.now())
        self.assertTrue(self.product.updated <= timezone.now())
        self.assertEqual(self.product.logo, "https://example.com/test.png")
        self.assertEqual(self.product.rotate_duration, 10.0)
        self.assertTrue(self.product.modified)

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")
