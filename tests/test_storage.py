"""
TODO
"""
from django.test import TestCase
from django.conf import settings
from images.storage import CloudflareImagesStorage


class CloudflareImageStorageTests(TestCase):
    """
    TODO
    """

    def setUp(self):
        self.storage = CloudflareImagesStorage()

    def test_has_service(self):
        service = self.storage.service
        self.assertTrue(service is not None)
