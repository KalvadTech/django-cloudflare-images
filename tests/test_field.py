"""
Tests related to the CloudflareImagesField
"""

from django.test import TestCase
from django.conf import settings
from cloudflare_images.field import CloudflareImagesField


class CloudflareImageFieldTests(TestCase):
    """
    Test case for the CloudflareImagesField
    TODO: add tests for CloudflareImagesFieldFile for url method
    """

    def test_default_variant(self):
        field = CloudflareImagesField()
        self.assertEqual(field.variant, "public")

    def test_custom_variant(self):
        variant = "custom"
        field = CloudflareImagesField(variant=variant)
        self.assertEqual(field.variant, variant)
