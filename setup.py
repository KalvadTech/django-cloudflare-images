import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='django-cloudflare-images',
    version='0.1',
    packages=['images'],
    description='Cloudflare Images integration for Django',
    long_description=README,
    author='Pierre Guillemot',
    author_email='pierre@kalvad.com',
    url='https://github.com/KalvadTech/django-cloudflare-images/',
    license='MIT',
    install_requires=[
        'Django>=4',
    ]
)

