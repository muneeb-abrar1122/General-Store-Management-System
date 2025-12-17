import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GeneralStore.settings')
django.setup()
from django.contrib.auth.models import User
try:
    u = User.objects.get(username='admin')
    print(f"User: {u.username}, Active: {u.is_active}, Staff: {u.is_staff}, Superuser: {u.is_superuser}")
    print(f"Password valid: {u.check_password('password123')}")
except User.DoesNotExist:
    print("User 'admin' does not exist.")
