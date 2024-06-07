"""
Tests related to the Config
"""

from cloudflare_images.config import Config
from django.test import TestCase, override_settings


class ConfigTests(TestCase):
    """
    Test case for Config
    """

    def setUp(self):
        self.config = Config()

    def test_account_id(self):
        account_id = self.config.account_id
        self.assertEqual(account_id, "account_id")

    def test_api_token(self):
        api_token = self.config.api_token
        self.assertEqual(api_token, "api_token")

    def test_account_hash(self):
        account_hash = self.config.account_hash
        self.assertEqual(account_hash, "account_hash")

    def test_domain(self):
        domain = self.config.domain
        self.assertEqual(domain, None)

    @override_settings(CLOUDFLARE_IMAGES_DOMAIN="example.com")
    def test_custom_domain(self):
        domain = self.config.domain
        self.assertEqual(domain, "example.com")

    def test_variant(self):
        variant = self.config.variant
        self.assertEqual(variant, "public")

    @override_settings(CLOUDFLARE_IMAGES_VARIANT="custom")
    def test_custom_variant(self):
        variant = self.config.variant
        self.assertEqual(variant, "custom")

    def test_api_timeout(self):
        api_timeout = self.config.api_timeout
        self.assertEqual(api_timeout, 60)

    @override_settings(CLOUDFLARE_IMAGES_API_TIMEOUT=100)
    def test_custom_api_timeout(self):
        api_timeout = self.config.api_timeout
        self.assertEqual(api_timeout, 100)

    def test_original_image(self):
        original_image = self.config.original_image
        self.assertEqual(original_image, False)

    @override_settings(CLOUDFLARE_IMAGES_ORIGINAL_IMAGE=True)
    def test_original_image_enabled(self):
        original_image = self.config.original_image
        self.assertEqual(original_image, True)
