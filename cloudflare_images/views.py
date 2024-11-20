"""
Views for the widget
"""

import json
from django.http import JsonResponse
from django.views.generic import View
from cloudflare_images.service import ApiException, CloudflareImagesService


class WidgetAPI(View):
    """
    View for the widget
    """

    def get(self, request):
        """
        Returns a one time upload URL
        """
        service = CloudflareImagesService()
        try:
            data = service.get_one_time_upload_url()
            return JsonResponse(data)
        except ApiException as e:
            return JsonResponse(json.loads(str(e)), status=400)

    def put(self, request):
        """
        TODO: save the new image and delete the old one if any
        Payload should be: model, field, ID, value
        """
        return JsonResponse({})

    def post(self, request):
        """
        TODO: use service.check_image_status for large(r) uploads
        """
        return JsonResponse({})
