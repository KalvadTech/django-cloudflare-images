"""
Contains the Cloudflare Image service which handles the API exchanges
"""

import requests
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

        response = requests.post(
            url, headers=headers, timeout=self.config.api_timeout, files=files
        )

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
        Retrieves a file and return its content, otherwise raise an exception
        """

        url = self.get_url(name, variant or self.config.variant)

        response = requests.get(url, timeout=self.config.api_timeout)

        status_code = response.status_code
        if status_code != 200:
            raise ApiException(response.content)

        return response.content

    def delete(self, name):
        """
        Deletes a file if it exists, otherwise raise an exception
        """

        url = "https://api.cloudflare.com/client/v4/accounts/{}/images/v1/{}".format(
            self.config.account_id, name
        )

        headers = {"Authorization": "Bearer {}".format(self.config.api_token)}

        response = requests.delete(
            url, timeout=self.config.api_timeout, headers=headers
        )

        status_code = response.status_code
        if status_code != 200:
            raise ApiException(str(response.text))

    def get_one_time_upload_url(self):
        """
        Direct Creator Upload endpoint
        Generates a one time upload URL
        """
        url = "https://api.cloudflare.com/client/v4/accounts/{}/images/v2/direct_upload".format(
            self.config.account_id
        )

        headers = {"Authorization": "Bearer {}".format(self.config.api_token)}

        response = requests.post(url, headers=headers, timeout=self.config.api_timeout)

        status_code = response.status_code
        if status_code != 200:
            raise ApiException(response.content)

        return response.json()

    def check_image_status(self, image_id):
        """
        Direct Creator Upload endpoint
        Checks the status of a new draft image record
        """
        url = "https://api.cloudflare.com/client/v4/accounts/{}/images/v1/{}".format(
            self.config.account_id, image_id
        )

        response = requests.get(url, timeout=self.config.api_timeout)

        status_code = response.status_code
        if status_code != 200:
            raise ApiException(response.content)

        return response.json()
