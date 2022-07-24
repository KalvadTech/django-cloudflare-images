import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md")).read()

setup(
    name="django-cloudflare-images",
    version="0.4.1",
    packages=["cloudflare_images"],
    description="Cloudflare Images integration for Django",
    long_description_content_type="text/markdown",
    long_description=README,
    author="Pierre Guillemot",
    author_email="pierre@kalvad.com",
    url="https://github.com/KalvadTech/django-cloudflare-images/",
    license="MIT",
    install_requires=["Django>=3", "requests>=2.20.0"],
    extras_require={"dev": ["black==22.6.0", "tox==3.25.1"]},
)
