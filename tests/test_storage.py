"""
Test related to the CloudflareImagesStorage
"""
from django.test import TestCase, override_settings
from django.conf import settings
from cloudflare_images.storage import CloudflareImagesStorage
from cloudflare_images.service import ApiException
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
        content.close()

    def test_open(self):
        name = "image_id"
        self.assertRaises(ApiException, self.storage.open, name)

    def test_delete(self):
        name = "image_id"
        self.assertRaises(ApiException, self.storage.delete, name)

    def test_url(self):
        name = "image_id"
        url = self.storage.url(name)
        hardcoded_url = "https://imagedelivery.net/account_hash/image_id/public"
        self.assertEqual(url, hardcoded_url)

    def test_url_with_variant(self):
        name = "image_id"
        variant = "custom"
        url = self.storage.url_with_variant(name, variant)
        hardcoded_url = "https://imagedelivery.net/account_hash/image_id/custom"
        self.assertEqual(url, hardcoded_url)

    @override_settings(CLOUDFLARE_IMAGES_DOMAIN="example.com")
    def test_url_with_custom_domain(self):
        name = "image_id"
        url = self.storage.url(name)
        hardcoded_url = "https://example.com/cdn-cgi/imagedelivery/account_hash/image_id/public"
        self.assertEqual(url, hardcoded_url)

    @override_settings(CLOUDFLARE_IMAGES_DOMAIN="example.com")
    def test_url_with_variant_with_custom_domain(self):
        name = "image_id"
        variant = "custom"
        url = self.storage.url_with_variant(name, variant)
        hardcoded_url = "https://example.com/cdn-cgi/imagedelivery/account_hash/image_id/custom"
        self.assertEqual(url, hardcoded_url)
