"""
Contains the Cloudflare Image service which handles the API exchanges
"""

import requests
from django.core.files.base import File
from cloudflare_images.config import Config


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
        Loads the configuration
        """
        self.config = Config()

    def upload(self, file):
        """
        Uploads a file and return its name, otherwise raise an exception
        """
        url = "https://api.cloudflare.com/client/v4/accounts/{}/images/v1".format(
            self.config.account_id
        )

        headers = {"Authorization": "Bearer {}".format(self.config.api_token)}

        files = {"file": file}

        response = requests.post(url, headers=headers, files=files)

        status_code = response.status_code
        if status_code != 200:
            raise ApiException(response.content)

        response_body = response.json()
        return response_body.get("result").get("id")

    def get_url(self, name, variant):
        """
        Returns the public URL for the given image ID
        """
        if self.config.domain:
            return "https://{}/cdn-cgi/imagedelivery/{}/{}/{}".format(
                self.config.domain, self.config.account_hash, name, variant
            )

        return "https://imagedelivery.net/{}/{}/{}".format(
            self.config.account_hash, name, variant
        )

    def open(self, name, variant=None):
        """
        Retrieves a file and turn it, otherwise raise an exception
        """

        url = self.get_url(name, variant or self.config.variant)

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
            self.config.account_id, name
        )

        headers = {"Authorization": "Bearer {}".format(self.config.api_token)}

        response = requests.delete(url, headers=headers)

        status_code = response.status_code
        if status_code != 200:
            raise ApiException(str(response.text))
