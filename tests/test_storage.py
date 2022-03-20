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

    def test_account_id(self):
        account_id = self.storage.account_id
        self.assertEqual(account_id, settings.CLOUDFLARE_IMAGES_ACCOUNT_ID)

    def test_api_token(self):
        api_token = self.storage.api_token
        self.assertEqual(api_token, settings.CLOUDFLARE_IMAGES_API_TOKEN)
