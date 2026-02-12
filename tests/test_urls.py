"""
Tests related to the CloudflareImagesWidget URL patterns
"""

from django.test import TestCase
from django.urls import reverse, resolve
from cloudflare_images.views import WidgetAPI


class UrlPatternTests(TestCase):
    """
    Test case for URL patterns
    """

    def test_widget_api_url_resolves(self):
        url = reverse("widget-api")
        self.assertEqual(url, "/cloudflare_images/api")

    def test_widget_api_url_resolves_to_view(self):
        resolved = resolve("/cloudflare_images/api")
        self.assertEqual(resolved.func.view_class, WidgetAPI)
