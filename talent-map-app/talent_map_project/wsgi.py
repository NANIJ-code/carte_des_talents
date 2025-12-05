"""
WSGI config for talent_map_project.

This module contains the WSGI application used by Django's runserver and any WSGI-compatible web servers.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talent_map_project.settings')

application = get_wsgi_application()