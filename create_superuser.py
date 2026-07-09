import os
import sys
import django
from pathlib import Path

# Ensure root directory is in sys.path to avoid ModuleNotFoundError
sys.path.append(str(Path(__file__).resolve().parent))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_booking.settings")
django.setup()

from django.contrib.auth.models import User
from django.db.utils import OperationalError, ProgrammingError

def create_admin():
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")

    try:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print(f"Superuser '{username}' created successfully.")
        else:
            print(f"Superuser '{username}' already exists.")
    except (OperationalError, ProgrammingError) as e:
        print(f"Database tables do not exist yet. Please run migrations first. (Detail: {e})")

if __name__ == "__main__":
    create_admin()
