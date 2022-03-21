"""
Test related to the CloudflareImagesStorage
"""
from django.test import TestCase
from django.conf import settings
from images.storage import CloudflareImagesStorage
from images.service import ApiException
from .utils import get_dummy_image, get_dummy_image_name


class CloudflareImageStorageTests(TestCase):
    """
    Test case for the CloudflareImagesStorage
    """

    def setUp(self):
        self.storage = CloudflareImagesStorage()

    def test_has_service(self):
        service = self.storage.service
        self.assertTrue(service is not None)

    def test_save(self):
        name = get_dummy_image_name()
        content = get_dummy_image()
        self.assertRaises(ApiException, self.storage.save, name, content)

    def test_open(self):
        name = "image_id"
        self.assertRaises(ApiException, self.storage.open, name)

    def test_delete(self):
        name = "image_id"
        self.assertRaises(ApiException, self.storage.delete, name)

    def test_url(self):
        name = "image_id"
        url = self.storage.url(name)
        self.assertTrue(url is not None)
