"""
Utils for running test
"""
from unittest.mock import MagicMock
import json


def get_dummy_image():
    """
    Returns the dummy image
    """
    return open("tests/python-logo.jpeg", "rb")


def get_dummy_image_name():
    """
    Returns the name of the dummy image
    """
    return "python-logo.jpeg"


def get_dummy_api_response(code, content, is_json=True):
    """
    Returns a dummy API response compliant with requests lib
    """
    response = MagicMock()
    response.status_code = code
    response.content = content
    if is_json:
        response.json = MagicMock(return_value=json.loads(content))

    return response
