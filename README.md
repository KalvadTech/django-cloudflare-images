# django-cloudflare-images

This is a Django library to add support to Cloudflare Images to the ImageField.

It supports:

 * Django 3
 * Django 4
 * Django 5

## Installation

```sh
pip install django-cloudflare-images
```

## Setup

You need to add the following your settings.py:


1. If you are running Django 4.2+:

```python
STORAGES = {"default": {"BACKEND": "cloudflare_images.storage.CloudflareImagesStorage"}}
```

2. Else:


```python
DEFAULT_FILE_STORAGE = "cloudflare_images.storage.CloudflareImagesStorage"
```

And then add the remaining of the configuration:

```python
CLOUDFLARE_IMAGES_ACCOUNT_ID = "XXX"
CLOUDFLARE_IMAGES_API_TOKEN = "YYY"
CLOUDFLARE_IMAGES_ACCOUNT_HASH = "ZZZ"
```

If you wish to use a default variant for a specific field you need to change your `ImageField` to a `CloudflareImagesField` see example below:

```python
from cloudflare_images.field import CloudflareImagesField
from django.db import models

class MyModel(models.Model):
    image = CloudflareImagesField(variant="custom")


```

Please note that you will need to migrate your model(s) once you swapped the field(s). No SQL will actually be applied (you can check by running `sqlmigrate <module> <number>`).

If you wish to use a custom domain to serve your images you need to add the following to your settings.py:

```python
CLOUDFLARE_IMAGES_DOMAIN = "example.com"
```

If you wish to use a default variant other than "public" to serve your images you need to add the following to your settings.py:

```python
CLOUDFLARE_IMAGES_VARIANT = "custom"
```

If you wish to override the default timeout of 60 seconds for API requests, you need to add the following to your settings.py:

```python
CLOUDFLARE_IMAGES_API_TIMEOUT = 120
```

## Direct Creator Upload

If you want to leverage Cloudflare's Direct Creator Upload (client side upload, similar to S3/Minio presigned URL concept), you need to do the following:

Modify your settings:

```python
INSTALLED_APPS = [
    "cloudflare_images",
]
```

Modify your urls:

```python
from cloudflare_images.views import WidgetAPI

# And add inside your router:
path("ext/cloudflare_images/api", WidgetAPI.as_view(), name="widget-api"),

```

**Please note that it is much safer to implement your own endpoint to retrieve the one time URL from cloudflare**

You can override the endpoint to use like so:

```python
CLOUDFLARE_IMAGES_UPLOAD_ENDPOINT="/my/endpoint/api"
```

Please refer to this file for the base implementation details: cloudflare_images/views.py

Modify/Add to your model:

```python
from cloudflare_images.field import CloudflareImageIDField

# in your model:
image = CloudflareImageIDField(variant="test")
```

If you are changing from a `CloudflareImagesField`, please note that you need to generate a migration (`python manage.py makemigrations`) and that this new field is **not backward compatible** in particular to access the `.url` field.

Modify your HTML template using a django form to load the JS/CSS:

```html
{{ form.media.js }}
{{ form.media.css }}
```

And you should be good to go. For basic troubleshooting, check your browser's console for hints or open a ticket.

## Development

Installing for development:

```sh
make install
```

Cleaning the installation:

```sh
make clean
```

Format the code:

```sh
make format
```

Check the code (for linting errors):

```sh
make check
```

Check the code (python type checker):

```sh
make static-check
```

Running all tests:

```sh
make test
```

Create a sdist+bdist package in dist/:

```sh
make package
```
