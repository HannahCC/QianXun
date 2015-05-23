"""
WSGI config for QianXun project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import os
import sys

apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)  
workspace = os.path.dirname(project)

if project not in sys.path:
    sys.path.append(project)
if workspace not in sys.path:
    sys.path.append(workspace)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "QianXun.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
