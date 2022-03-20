"""
TODO
"""

from django.conf import settings
from django.core.files.storage import Storage

class CloudflareImageStorage(Storage):
    """
    TODO
    """

    def __init__(self):
        """
        TODO
        """
        super().__init__()

        self.account_id = settings.get('CLOUDFLARE_IMAGES_ACCOUNT_ID')
        self.api_token = settings.get('CLOUDFLARE_IMAGES_API_TOKEN')

        print(self.account_id)
        print(self.api_token)
