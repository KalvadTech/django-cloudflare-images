"""
Custom widget for Direct Creator Uploads
"""

from django.forms import ClearableFileInput


class CloudflareImagesWidget(ClearableFileInput):
    """
    Widget
    """

    template_name = "widget.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        instance  = self.form_instance.instance
        context['app_label'] = instance._meta.app_label
        context['model'] = instance._meta.model_name
        context['id'] = str(instance.id)
        return context

    class Media:
        """
        Inner class defining the static assets for the widget
        """

        css = {"all": ["static/css/widget.css"]}
        js = ["static/js/widget.js"]
