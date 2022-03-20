"""
TODO
"""

from django.conf import settings
import requests


class CloudflareImagesService:
    """
    TODO
    """

    def __init__(self):
        """
        Retrieves django settings
        """
        super().__init__()

        self.account_id = settings.CLOUDFLARE_IMAGES_ACCOUNT_ID
        self.api_token = settings.CLOUDFLARE_IMAGES_API_TOKEN

    def upload_file(self, file):
        """
        TODO
        """
        url = "https://api.cloudflare.com/client/v4/accounts/{}/images/v1".format(
            self.account_id
        )

        headers = {
            "Authorization": "Bearer {}".format(self.api_token)
        }

        files = {'file': open(file)}

        response = requests.post(url, headers=headers, files=files)

        status_code = response.status_code
        if status_code != 200:
            print(response.text)
            raise Exception("TODO")
