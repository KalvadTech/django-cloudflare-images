## 0.4.1

### Misc

 * Set the minimum requirements for `Django` to 3.0

## 0.4.0

### Features

 * Added support for global custom variant (to override default "public")

### Bugfix

 * Fixed a rare bug where Cloudflare would return a 502 timeout (HTML page, not JSON) during an upload and the service would explode when trying to parse json

## 0.3.1

### Misc

 * Set the minimum requirements for `requests` to 2.20.0 (latest secure release to date)

## 0.3.0

### Features

 * Added support for custom domain name when serving images

## 0.2.0

### Features

 * Added support for variants at the field level

## 0.1.0

### Features

 * First release
