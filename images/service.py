"""
Contains the Cloudflare Image service which handles the API exchanges
"""

from django.conf import settings
import requests


class CloudflareImagesService:
    """
    API client for Cloudflare Images
    """

    def __init__(self):
        """
        Retrieves django settings
        """
        super().__init__()

        self.account_id = settings.CLOUDFLARE_IMAGES_ACCOUNT_ID
        self.api_token = settings.CLOUDFLARE_IMAGES_API_TOKEN

    def upload(self, file):
        """
        Uploads a file and return its name, otherwise raise an exception
        """
        url = "https://api.cloudflare.com/client/v4/accounts/{}/images/v1".format(
            self.account_id
        )

        headers = {"Authorization": "Bearer {}".format(self.api_token)}

        files = {"file": file}

        response = requests.post(url, headers=headers, files=files)
        response_body = response.json()

        status_code = response.status_code
        if status_code != 200:
            raise Exception(str(response_body.get("errors")))

        return response_body.get("result").get("filename")
