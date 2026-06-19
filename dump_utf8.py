import os
import django

os.environ.pop('DATABASE_URL', None)  # Force SQLite

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodorder.settings')
django.setup()

from django.core.management import call_command

with open('datadump_utf8.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', exclude=['auth.permission', 'contenttypes'], stdout=f)

print("Data dumped to datadump_utf8.json with UTF-8 encoding.")
