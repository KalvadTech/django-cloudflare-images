"""
Views for the widget
"""

import json
from django.http import HttpRequest, JsonResponse
from django.apps import apps
from django.views.generic import View
from cloudflare_images.service import ApiException, CloudflareImagesService


class WidgetAPI(View):
    """
    View for the widget
    """

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Returns a one time upload URL.
        This endpoint has no security and should just be used as an example
        on how to implement your own. See the Config object's documentation.
        """
        service = CloudflareImagesService()
        try:
            data = service.get_one_time_upload_url()
            return JsonResponse(data)
        except ApiException as e:
            return JsonResponse(json.loads(str(e)), status=400)
