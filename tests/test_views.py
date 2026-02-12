"""
Tests related to the CloudflareImagesWidget Views
"""

from unittest.mock import Mock, patch
from django.test import TestCase, RequestFactory
from django.http import JsonResponse
from cloudflare_images.views import WidgetAPI
from cloudflare_images.service import ApiException


class WidgetAPITests(TestCase):
    """
    Test case for the WidgetAPI view
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.view = WidgetAPI()

    @patch("cloudflare_images.views.CloudflareImagesService")
    def test_get_success(self, mock_service):
        mock_service.return_value.get_one_time_upload_url.return_value = {
            "uploadURL": "https://upload.example.com/token"
        }

        request = self.factory.get("/")
        response = self.view.get(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)

    @patch("cloudflare_images.views.CloudflareImagesService")
    def test_get_api_exception(self, mock_service):
        mock_service.return_value.get_one_time_upload_url.side_effect = ApiException(
            '{"error": "Invalid token"}'
        )

        request = self.factory.get("/")
        response = self.view.get(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)

    @patch("cloudflare_images.views.CloudflareImagesService")
    def test_get_api_exception_with_json_parsing(self, mock_service):
        mock_service.return_value.get_one_time_upload_url.side_effect = ApiException(
            '{"error": {"message": "Rate limit exceeded"}}'
        )

        request = self.factory.get("/")
        response = self.view.get(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)
