"""
Contains the Cloudflare Image service which handles the API exchanges
"""

from django.core.files.base import File
from django.conf import settings
import requests


class ApiException(Exception):
    """
    Exception raised by Cloudflare Images API
    """

    pass


class CloudflareImagesService:
    """
    API client for Cloudflare Images
    """

    def __init__(self):
        """
        Retrieves django settings
        """
        self.account_id = settings.CLOUDFLARE_IMAGES_ACCOUNT_ID
        self.api_token = settings.CLOUDFLARE_IMAGES_API_TOKEN
        self.account_hash = settings.CLOUDFLARE_IMAGES_ACCOUNT_HASH

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
            raise ApiException(str(response_body.get("errors")))

        return response_body.get("result").get("id")

    def get_url(self, name, variant="public"):
        """
        Returns the public URL for the given image ID
        """
        return "https://imagedelivery.net/{}/{}/{}".format(
            self.account_hash, name, variant
        )

    def open(self, name, variant="public"):
        """
        Retrieves a file and turn it, otherwise raise an exception
        """

        url = self.get_url(name, variant)

        response = requests.get(url)

        status_code = response.status_code
        if status_code != 200:
            raise ApiException(response.content)

        return File(response.content, name=name)

    def delete(self, name):
        """
        Deletes a file if it exists, otherwise raise an exception
        """

        url = "https://api.cloudflare.com/client/v4/accounts/{}/images/v1/{}".format(
            self.account_id, name
        )

        headers = {"Authorization": "Bearer {}".format(self.api_token)}

        response = requests.delete(url, headers=headers)

        status_code = response.status_code
        if status_code != 200:
            raise ApiException(str(response.text))
