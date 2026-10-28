"""
Tests related to the Config
"""

from django.core.exceptions import ImproperlyConfigured
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

    def test_api_timeout(self):
        api_timeout = self.config.api_timeout
        self.assertEqual(api_timeout, 60)

    @override_settings(CLOUDFLARE_IMAGES_API_TIMEOUT=100)
    def test_custom_api_timeout(self):
        api_timeout = self.config.api_timeout
        self.assertEqual(api_timeout, 100)

    def test_upload_endpoint(self):
        endpoint = self.config.upload_endpoint
        self.assertEqual(endpoint, "/ext/cloudflare_images/api")

    @override_settings(CLOUDFLARE_IMAGES_UPLOAD_ENDPOINT="/test/api")
    def test_custom_upload_endpoint(self):
        endpoint = self.config.upload_endpoint
        self.assertEqual(endpoint, "/test/api")

    def test_signing_key(self):
        signing_key = self.config.signing_key
        self.assertIsNone(signing_key)

    @override_settings(CLOUDFLARE_IMAGES_SIGNING_KEY="signing_key")
    def test_custom_signing_key(self):
        signing_key = self.config.signing_key
        self.assertEqual(signing_key, "signing_key")

    def test_signed_url_ttl(self):
        ttl = self.config.signed_url_ttl
        self.assertEqual(ttl, 86400)

    @override_settings(CLOUDFLARE_IMAGES_SIGNED_URL_TTL=120)
    def test_custom_signed_url_ttl(self):
        ttl = self.config.signed_url_ttl
        self.assertEqual(ttl, 120)

    @override_settings(CLOUDFLARE_IMAGES_SIGNED_URL_TTL=0)
    def test_invalid_signed_url_ttl(self):
        self.assertRaises(ImproperlyConfigured, lambda: self.config.signed_url_ttl)

    @override_settings(CLOUDFLARE_IMAGES_SIGNED_URL_TTL="not-a-number")
    def test_non_numeric_signed_url_ttl(self):
        self.assertRaises(ImproperlyConfigured, lambda: self.config.signed_url_ttl)
