"""
ASGI config for myasgi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

import django
from django.core.asgi import get_asgi_application
from mywebsocket.middleware import websockets

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myasgi.settings')

django.setup()
application = get_asgi_application()
application = websockets(application)

#pip install uvicorn[standard]