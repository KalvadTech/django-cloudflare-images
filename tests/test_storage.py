"""
Test related to the CloudflareImagesStorage
"""
from django.test import TestCase
from django.conf import settings
from django.core.files.base import ContentFile
from images.storage import CloudflareImagesStorage
from images.service import ApiException


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
        name = "test.jpg"
        content = ContentFile("this is a test image")
        self.assertRaises(ApiException, self.storage.save, name, content)

    def test_open(self):
        name = "image_id"
        self.assertRaises(ApiException, self.storage.open, name)
