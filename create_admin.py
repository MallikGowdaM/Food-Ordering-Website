import os
import django

os.environ['DATABASE_URL'] = 'postgresql://postgres.wcfvnktgdqtqjgdyotjm:mALLIK7022!@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodorder.settings")
django.setup()

from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created: admin / admin123")
else:
    print("Superuser 'admin' already exists.")
