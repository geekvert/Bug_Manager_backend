"""
ASGI config for Bug_Manager project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

# deafult code
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bug_Manager.settings')

application = get_asgi_application()


# experimental stuff
# import os
# import django
# from channels.routing import get_default_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bug_Manager.settings")
# django.setup()
# application = get_default_application()
