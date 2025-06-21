# crear_admin.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SistemaLicoreria.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin1234')
    print("Superusuario creado exitosamente.")
else:
    print("El superusuario ya existe.")
