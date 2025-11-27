"""
Custom widget for Direct Creator Uploads
"""

from django.forms import ClearableFileInput


class CloudflareImagesWidget(ClearableFileInput):
    """
    Widget
    """

    template_name = "widget.html"

    def value_from_datadict(self, data, files, name):
        return data.get(name)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["value"] = value
        return context

    class Media:
        """
        Inner class defining the static assets for the widget
        """

        css = {"all": ["css/widget.css"]}
        js = ["js/widget.js"]
