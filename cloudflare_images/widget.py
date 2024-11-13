"""
Custom widget for Direct Creator Uploads
"""

from django.forms import ClearableFileInput


class CloudflareImagesWidget(ClearableFileInput):
    """
    Widget
    """

    template_name = "widget.html"

    class Media:
        """
        Inner class defining the static assets for the widget
        """

        css = {"all": ["static/css/widget.css"]}
        js = ["static/js/widget.js"]
