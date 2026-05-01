"""
Script to assign generated images to FoodItem database records.
Run with: python assign_images.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodorder.settings')
django.setup()

from store.models import FoodItem

# Maps food item name → image filename in media/food_images/
IMAGE_MAP = {
    'Veg Spring Rolls':       'veg_spring_rolls.png',
    'Chicken Tikka':          'chicken_tikka.png',
    'Paneer Tikka':           'paneer_tikka.png',
    'Garlic Mushrooms':       'garlic_mushrooms.png',
    'Butter Chicken':         'butter_chicken.png',
    'Dal Makhani':            'dal_makhani.png',
    'Paneer Butter Masala':   'paneer_butter_masala.png',
    'Chicken Biryani':        'chicken_biryani.png',
    'Palak Paneer':           'palak_paneer.png',
    'Mutton Rogan Josh':      'mutton_rogan_josh.png',
    'Samosa (2 pcs)':         'samosa.png',
    'Aloo Tikki':             'aloo_tikki.png',
    'Pav Bhaji':              'pav_bhaji.png',
    'French Fries':           'french_fries.png',
    'Gulab Jamun':            'gulab_jamun.png',
    'Chocolate Brownie':      'chocolate_brownie.png',
    'Mango Kulfi':            'mango_kulfi.png',
    # Rasgulla, Mango Lassi, Masala Chai, Fresh Lime Soda, Cold Coffee
    # will use emoji placeholders (image quota exhausted)
}

updated = 0
for name, filename in IMAGE_MAP.items():
    try:
        item = FoodItem.objects.get(name=name)
        item.image = f'food_images/{filename}'
        item.save()
        print(f'[OK] {name} -> food_images/{filename}')
        updated += 1
    except FoodItem.DoesNotExist:
        print(f'[SKIP] Not found: {name}')

print(f'\nDone! Updated {updated} food items with images.')
