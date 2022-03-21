"""
Tests related to the CloudflareImagesService
"""

from django.test import TestCase
from django.conf import settings
from images.service import CloudflareImagesService, ApiException
from .utils import get_dummy_image


class CloudflareImageServiceTests(TestCase):
    """
    Test case for the CloudflareImagesService
    """

    def setUp(self):
        self.service = CloudflareImagesService()

    def test_account_id(self):
        account_id = self.service.account_id
        self.assertEqual(account_id, settings.CLOUDFLARE_IMAGES_ACCOUNT_ID)

    def test_api_token(self):
        api_token = self.service.api_token
        self.assertEqual(api_token, settings.CLOUDFLARE_IMAGES_API_TOKEN)

    def test_account_hash(self):
        account_hash = self.service.account_hash
        self.assertEqual(account_hash, settings.CLOUDFLARE_IMAGES_ACCOUNT_HASH)

    def test_upload(self):
        file = get_dummy_image()
        self.assertRaises(ApiException, self.service.upload, file)

    def test_open_default_variant(self):
        name = "id_image"
        self.assertRaises(ApiException, self.service.open, name)

    def test_delete(self):
        name = "id_image"
        self.assertRaises(ApiException, self.service.delete, name)

    def test_get_url(self):
        name = "id_image"
        url = self.service.get_url(name)
        self.assertTrue(url is not None)
