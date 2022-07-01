"""
Tests related to the Config
"""

from django.test import TestCase, override_settings
from cloudflare_images.config import Config


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
