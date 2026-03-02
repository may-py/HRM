from .base import *
import os


DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'change-me-on-the-droplet-immediately')

ALLOWED_HOSTS = ['your_droplet_ip', 'yourdomain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# 3. STATIC & MEDIA FILES
# This is where Nginx will look for your CSS/JS
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

# 4. SECURITY HEADERS (Recommended for Droplets)
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'