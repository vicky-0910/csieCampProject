from csieCampProject.wsgi import application
app = application

"""
import os
import django
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

def apply_migrations():
    try:
        call_command("migrate", interactive=False, run_syncdb=True)
        logger.info("Django migrations applied successfully.")
    except Exception as e:
        logger.error(f"Failed to apply migrations: {e}")

apply_migrations()
"""
