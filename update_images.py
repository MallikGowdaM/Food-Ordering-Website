import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodorder.settings')
django.setup()

from store.models import FoodItem

def update_images():
    try:
        mango = FoodItem.objects.get(name__icontains='Mango Lassi')
        mango.image = 'food_images/mango_lassi.jpg'
        mango.save()
        print("Updated Mango Lassi image")
    except FoodItem.DoesNotExist:
        print("Mango Lassi not found")

    try:
        rasgulla = FoodItem.objects.get(name__icontains='Rasgulla')
        rasgulla.image = 'food_images/rasgulla.jpg'
        rasgulla.save()
        print("Updated Rasgulla image")
    except FoodItem.DoesNotExist:
        print("Rasgulla not found")

if __name__ == '__main__':
    update_images()
