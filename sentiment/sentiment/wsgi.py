"""
WSGI config for sentiment project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys
root = os.path.join(os.path.dirname(__file__),'..')
sys.path.insert(0,root)


from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sentiment.settings")

application = get_wsgi_application()

