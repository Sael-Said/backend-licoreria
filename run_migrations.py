# run_migrations.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SistemaLicoreria.settings")
django.setup()

from django.core.management import call_command

call_command("makemigrations")
call_command("migrate")
