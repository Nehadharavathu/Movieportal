import os
import django
import sys
from pathlib import Path

# Add root directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_booking.settings")
django.setup()

from django.contrib.admin.sites import site

print("Admin site modules loaded successfully!")
for model, admin_class in site._registry.items():
    print(f"Registered: {model.__name__} -> {admin_class.__class__.__name__}")
