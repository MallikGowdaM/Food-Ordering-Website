"""
Script to assign remaining missing images to FoodItem records.
Run with: python assign_remaining_images.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodorder.settings')
django.setup()

from store.models import FoodItem

REMAINING_MAP = {
    'Rasgulla':      'rasgulla.png',
    'Mango Lassi':   'mango_lassi.png',
    'Masala Chai':   'masala_chai.png',
    'Fresh Lime Soda': 'fresh_lime_soda.png',
    'Cold Coffee':   'cold_coffee.png',
}

updated = 0
for name, filename in REMAINING_MAP.items():
    try:
        item = FoodItem.objects.get(name=name)
        item.image = f'food_images/{filename}'
        item.save()
        print(f'[OK] {name} -> food_images/{filename}')
        updated += 1
    except FoodItem.DoesNotExist:
        print(f'[SKIP] Not found: {name}')

print(f'\nDone! Updated {updated} food items with images.')
