"""
Tests related to the package contents
"""

from importlib.resources import files

from django.test import SimpleTestCase


class PackageTests(SimpleTestCase):
    """
    Test case for the package contents
    """

    def test_py_typed_marker(self):
        self.assertTrue(files("cloudflare_images").joinpath("py.typed").is_file())

    def test_template_and_static_files(self):
        package = files("cloudflare_images")
        for path in (
            "templates/widget.html",
            "static/css/widget.css",
            "static/js/widget.js",
        ):
            with self.subTest(path=path):
                self.assertTrue(package.joinpath(path).is_file())
