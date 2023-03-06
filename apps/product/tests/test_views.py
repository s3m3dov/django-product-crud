from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from apps.product.forms import ProductForm
from apps.product.models import Product
from apps.product.tasks import ImageUploadTask

IMAGE_BYTES = b"""0xff, 0xff, 0xff, 0xff, 0xf8, 0xff, 0xff, 0xff, 0xff, 0xf8, 0xff, 0xff, 0xff, 0xff, 0xf8, 0xff, 
0xff, 0xff, 0xff, 0xf8, 0xff, 0xff, 0xff, 0xff, 0xf8, 0xff, 0xff, 0xff, 0xff, 0xf8, 0xff, 0xff, 
0xff, 0xff, 0xf8, 0xff, 0xff, 0xff, 0xff, 0xf8, 0xff, 0xff, 0xff, 0xff, 0xf8, 0xf0, 0x3f, 0x03, 
0xe0, 0x78, 0xe0, 0x0c, 0x01, 0xc0, 0x18, 0xc0, 0x08, 0x00, 0x80, 0x08, 0x87, 0x80, 0x70, 0x07, 
0x08, 0x8f, 0xc0, 0xfc, 0x0f, 0x80, 0x8f, 0xe1, 0xfc, 0x1f, 0xc0, 0x8f, 0xe1, 0xfc, 0x3f, 0xc0, 
0x8f, 0xe3, 0xfc, 0x3f, 0xc0, 0x8f, 0xc3, 0xfc, 0x7f, 0x80, 0x87, 0xc7, 0xf8, 0x7f, 0x88, 0xc7, 
0x87, 0xf8, 0xff, 0x08, 0xc3, 0x0f, 0xf0, 0xff, 0x18, 0xe1, 0x1f, 0xe1, 0xfe, 0x18, 0xf0, 0x1f, 
0xe3, 0xfc, 0x38, 0xf0, 0x3f, 0xc3, 0xfc, 0x38, 0xf8, 0x3f, 0xc3, 0xf8, 0x78, 0xf8, 0x3f, 0x87, 
0xf8, 0xf8, 0xfc, 0x3f, 0x87, 0xf0, 0xf8, 0xfc, 0x3f, 0x03, 0xf1, 0xf8, 0xfe, 0x1e, 0x01, 0xe1, 
0xf8, 0xff, 0x00, 0x00, 0x03, 0xf8, 0xff, 0x00, 0x30, 0x07, 0xf8, 0xff, 0xc0, 0x78, 0x0f, 0xf8, 
0xff, 0xff, 0xff, 0xff, 0xf8, 0xff, 0xff, 0xff, 0xff, 0xf8, 0xff, 0xff, 0xff, 0xff, 0xf8, 0xff, 
0xff, 0xff, 0xff, 0xf8, 0xff, 0xff, 0xff, 0xff, 0xf8"""


class ProductListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("product:product-list")

    def test_product_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product-list.html")
        self.assertContains(response, "Products")

    def test_product_list_view_filter_modified_true(self):
        Product.objects.create(name="Product 1", modified=True)
        Product.objects.create(name="Product 2", modified=False)
        response = self.client.get(self.url, {"modified": "true"})
        self.assertContains(response, "Product 1")
        self.assertNotContains(response, "Product 2")

    def test_product_list_view_filter_modified_false(self):
        Product.objects.create(name="Product 1", modified=True)
        Product.objects.create(name="Product 2", modified=False)
        response = self.client.get(self.url, {"modified": "false"})
        self.assertContains(response, "Product 2")
        self.assertNotContains(response, "Product 1")


class ProductCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("product:product-create")

    def test_get_product_create_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product-create.html")
        self.assertIsInstance(response.context["form"], ProductForm)

    @patch.object(ImageUploadTask, "delay")
    def test_post_product_create_view(self, mock_task_delay):
        simple_file = SimpleUploadedFile(
            "file.jpg", IMAGE_BYTES, content_type="image/jpeg"
        )
        data = {
            "name": "Product Test",
            "description": "This is a test product.",
            "logo_file": simple_file,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("product:product-list"))
        self.assertEqual(Product.objects.count(), 1)


class ProductDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name="Product Test")
        self.url = reverse(
            "product:product-detail", kwargs={"pk": self.product.uuid}
        )

    def test_product_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product-detail.html")
        self.assertEqual(response.context["product"], self.product)


class ProductUpdateViewTestCase(TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.success_url = reverse("product:product-list")

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            logo=None,
            rotate_duration=None,
            modified=False,
        )
        self.url = reverse(
            "product:product-update", args=[str(self.product.uuid)]
        )

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product-update.html")

    def test_post(self):
        logo_file = SimpleUploadedFile(
            "logo.png",
            content=IMAGE_BYTES,
            content_type="image/png",
        )
        data = {"name": "Updated Test Product", "logo_file": logo_file}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.success_url)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Test Product")
        self.assertTrue(self.product.modified)

    def test_post_with_already_modified_product(self):
        self.product.modified = True
        self.product.save()
        data = {"name": "Updated Test Product"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Product has already been modified")

    def test_post_with_invalid_form_data(self):
        data = {"name": ""}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
        self.assertFalse(self.product.modified)

    def test_post_with_invalid_logo_file(self):
        logo_file = SimpleUploadedFile(
            "logo.png",
            content=b"invalid image",
            content_type="image/png",
        )
        data = {"name": "Updated Test Product", "logo_file": logo_file}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.product.modified)


class ProductDeleteViewTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product")
        self.url = reverse("product:product-delete", args=[self.product.uuid])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product-delete.html")

    def test_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("product:product-list"))
        self.assertFalse(
            Product.objects.filter(uuid=self.product.uuid).exists()
        )
