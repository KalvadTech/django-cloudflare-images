# django-cloudflare-images

This is a Django library to add support to Cloudflare Images to the ImageField.

It supports:

 * Django 3
 * Django 4
 * Django 5
 * Django 6

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

If you wish to serve private images, add your signing key from the Cloudflare dashboard (Images > Keys):

```python
CLOUDFLARE_IMAGES_SIGNING_KEY = "..."
```

Signed URLs are valid for 24 hours by default. You can override this globally in seconds:

```python
CLOUDFLARE_IMAGES_SIGNED_URL_TTL = 3600
```

## Checking if an Image Exists

You can check if an image exists in Cloudflare Images using the storage's `exists()` method:

```python
from django.core.files.storage import default_storage

if default_storage.exists("image_id"):
    print("Image exists!")
else:
    print("Image not found")
```

**Note:** This method makes an HTTP API call to Cloudflare on every invocation. If you need to check many images, consider implementing your own caching layer to reduce API calls.

## Private Images and Signed URLs

Cloudflare Images can serve private images that require a signed URL. Add your signing key to your settings (see [Setup](#setup)):

```python
CLOUDFLARE_IMAGES_SIGNING_KEY = "..."
```

### Server-side uploads

Use a storage configured with `require_signed_urls=True` and attach it to your field:

```python
from cloudflare_images.field import CloudflareImagesField
from cloudflare_images.storage import CloudflareImagesStorage

private_storage = CloudflareImagesStorage(require_signed_urls=True)

class Document(models.Model):
    image = CloudflareImagesField(storage=private_storage)
```

With this storage:

- uploads are created with `requireSignedURLs=true`;
- `document.image.url` returns a signed URL;
- `storage.open()` and `storage.size()` use signed URLs internally.

If the whole project uses private images, you can configure the default storage instead of attaching a storage to each field (Django 4.2+):

```python
STORAGES = {
    "default": {
        "BACKEND": "cloudflare_images.storage.CloudflareImagesStorage",
        "OPTIONS": {"require_signed_urls": True},
    },
}
```

You can generate a signed URL explicitly, with a custom lifetime in seconds:

```python
url = document.image.signed_url(expires_in=300)
# or, without a field:
url = private_storage.signed_url("image_id", "public", expires_in=300)
```

If no `expires_in` is provided, `CLOUDFLARE_IMAGES_SIGNED_URL_TTL` is used (24 hours by default).

### Direct Creator Upload

To create private images with the direct upload flow, subclass the provided view and request private uploads:

```python
from cloudflare_images.views import WidgetAPI

class PrivateWidgetAPI(WidgetAPI):
    def get_upload_options(self, request):
        return {"require_signed_urls": True}
```

Use `PrivateWidgetAPI` in your URL configuration instead of `WidgetAPI`, and generate signed preview URLs by passing `signed=True` to the widget:

```python
from django import forms

from cloudflare_images.widget import CloudflareImagesWidget

class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ["image"]
        widgets = {"image": CloudflareImagesWidget(signed=True)}
```

After a private upload, the widget displays the image ID without a link until the form is saved and the page is rendered again, at which point the preview URL is signed.

If you use `CloudflareImageIDField`, you can generate the URL yourself:

```python
from cloudflare_images.service import CloudflareImagesService

@property
def image_url(self):
    if not self.image:
        return None
    return CloudflareImagesService().get_signed_url(self.image, "public")
```

**Caveats:**

- Generate signed URLs when rendering; do not store them, as they expire.
- Rotating the signing key invalidates all existing signed URLs.
- Cloudflare's custom paths feature does not support private images.
- Images uploaded with a custom ID cannot be made private with signed URLs.

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
CLOUDFLARE_IMAGES_UPLOAD_ENDPOINT = "/my/endpoint/api"
```

Please refer to [this file](https://github.com/KalvadTech/django-cloudflare-images/blob/468fd55f59a9edac4ecd2b25c361308994b60ef6/cloudflare_images/views.py) for the base implementation details

Modify/Add to your model:

```python
from cloudflare_images.field import CloudflareImageIDField

# in your model:
image = CloudflareImageIDField(variant="test")
```

If you are changing from a `CloudflareImagesField`, please note that you need to generate a migration (`python manage.py makemigrations`) and that this new field is **not backward compatible** in particular to access the `.url` field. To access your field's URL it is recommended to write a helper (or use a custom mixin) in your model like so:

```python
from cloudflare_images.service import CloudflareImagesService

    @property
    def image_url(self) -> str | None:
        if not self.image:
            return None
        service = CloudflareImagesService()
        return service.get_url(self.image, "public") # or any variant that you want
```

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
