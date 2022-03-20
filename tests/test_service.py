"""
TODO
"""
from django.test import TestCase
from django.conf import settings
from images.service import CloudflareImagesService


class CloudflareImageServiceTests(TestCase):
    """
    TODO
    """

    def setUp(self):
        self.service = CloudflareImagesService()

    def test_account_id(self):
        account_id = self.service.account_id
        self.assertEqual(account_id, settings.CLOUDFLARE_IMAGES_ACCOUNT_ID)

    def test_api_token(self):
        api_token = self.service.api_token
        self.assertEqual(api_token, settings.CLOUDFLARE_IMAGES_API_TOKEN)
