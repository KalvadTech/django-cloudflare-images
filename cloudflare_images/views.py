"""
Views for the widget
"""

import json
from django.http import JsonResponse
from django.apps import apps
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from cloudflare_images.service import ApiException, CloudflareImagesService

# TODO: to remove
@method_decorator(csrf_exempt, name="dispatch")
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
        data = json.loads(request.body) # TODO: Use a form to validate payload
        Model = apps.get_model(data.get("app_label"), data.get("model"))
        instance = Model.objects.get(pk=data.get("id"))
        print(instance)
        print(getattr(instance, data.get("field")))
        setattr(instance, data.get("field"), data.get("value"))
        instance.save()
        return JsonResponse({})

    def post(self, request):
        """
        TODO: use service.check_image_status for large(r) uploads
        """
        return JsonResponse({})
