"""Management command to populate the database with sample food items."""

from django.core.management.base import BaseCommand
from store.models import FoodItem


SAMPLE_ITEMS = [
    # Starters
    {'name': 'Veg Spring Rolls', 'category': 'starters', 'price': 149, 'image': 'food_images/veg_spring_rolls.png', 'description': 'Crispy rolls stuffed with fresh vegetables and served with sweet chilli dip.'},
    {'name': 'Chicken Tikka', 'category': 'starters', 'price': 249, 'image': 'food_images/chicken_tikka.png', 'description': 'Tender chicken marinated in yogurt and spices, grilled to perfection.'},
    {'name': 'Paneer Tikka', 'category': 'starters', 'price': 219, 'image': 'food_images/paneer_tikka.png', 'description': 'Soft cottage cheese cubes marinated in spiced yogurt, chargrilled.'},
    {'name': 'Garlic Mushrooms', 'category': 'starters', 'price': 179, 'image': 'food_images/garlic_mushrooms.png', 'description': 'Button mushrooms sauteed in garlic butter with fresh herbs.'},

    # Main Course
    {'name': 'Butter Chicken', 'category': 'main_course', 'price': 299, 'image': 'food_images/butter_chicken.png', 'description': 'Succulent chicken in rich, creamy tomato-based gravy with butter.'},
    {'name': 'Dal Makhani', 'category': 'main_course', 'price': 229, 'image': 'food_images/dal_makhani.png', 'description': 'Slow-cooked black lentils in a buttery, creamy tomato gravy.'},
    {'name': 'Paneer Butter Masala', 'category': 'main_course', 'price': 269, 'image': 'food_images/paneer_butter_masala.png', 'description': 'Soft paneer cubes in a velvety, mildly spiced tomato-cashew gravy.'},
    {'name': 'Chicken Biryani', 'category': 'main_course', 'price': 349, 'image': 'food_images/chicken_biryani.png', 'description': 'Fragrant basmati rice layered with spiced chicken and caramelised onions.'},
    {'name': 'Palak Paneer', 'category': 'main_course', 'price': 239, 'image': 'food_images/palak_paneer.png', 'description': 'Cottage cheese in a smooth, freshly pureed spinach gravy.'},
    {'name': 'Mutton Rogan Josh', 'category': 'main_course', 'price': 389, 'image': 'food_images/mutton_rogan_josh.png', 'description': 'Slow-braised mutton in aromatic Kashmiri spices and deep red gravy.'},

    # Snacks
    {'name': 'Samosa (2 pcs)', 'category': 'snacks', 'price': 49, 'image': 'food_images/samosa.png', 'description': 'Crispy pastry triangles stuffed with spiced potatoes and peas.'},
    {'name': 'Aloo Tikki', 'category': 'snacks', 'price': 79, 'image': 'food_images/aloo_tikki.png', 'description': 'Golden potato patties with chutneys and sev.'},
    {'name': 'Pav Bhaji', 'category': 'snacks', 'price': 129, 'image': 'food_images/pav_bhaji.png', 'description': 'Spiced mixed vegetable mash served with buttered pav rolls.'},
    {'name': 'French Fries', 'category': 'snacks', 'price': 99, 'image': 'food_images/french_fries.png', 'description': 'Golden, crispy fries served with ketchup and mayo.'},

    # Desserts
    {'name': 'Gulab Jamun', 'category': 'desserts', 'price': 89, 'image': 'food_images/gulab_jamun.png', 'description': 'Soft milk-solid dumplings soaked in rose-scented sugar syrup.'},
    {'name': 'Chocolate Brownie', 'category': 'desserts', 'price': 129, 'image': 'food_images/chocolate_brownie.png', 'description': 'Rich, fudgy chocolate brownie served warm with a scoop of vanilla ice cream.'},
    {'name': 'Mango Kulfi', 'category': 'desserts', 'price': 99, 'image': 'food_images/mango_kulfi.png', 'description': 'Dense, creamy traditional Indian ice cream with alphonso mango.'},
    {'name': 'Rasgulla', 'category': 'desserts', 'price': 79, 'image': '', 'description': 'Light, spongy cheese balls in a light sugar syrup.'},

    # Beverages
    {'name': 'Mango Lassi', 'category': 'beverages', 'price': 89, 'image': '', 'description': 'Chilled yogurt drink blended with sweet Alphonso mango.'},
    {'name': 'Masala Chai', 'category': 'beverages', 'price': 49, 'image': '', 'description': 'Spiced Indian tea brewed with ginger, cardamom, and milk.'},
    {'name': 'Fresh Lime Soda', 'category': 'beverages', 'price': 59, 'image': '', 'description': 'Refreshing chilled lime juice topped with sparkling soda.'},
    {'name': 'Cold Coffee', 'category': 'beverages', 'price': 119, 'image': '', 'description': 'Blended iced coffee with milk and a hint of vanilla.'},
]


class Command(BaseCommand):
    help = 'Populate the database with sample food items'

    def handle(self, *args, **kwargs):
        created = 0
        for item_data in SAMPLE_ITEMS:
            _, was_created = FoodItem.objects.get_or_create(
                name=item_data['name'],
                defaults={
                    'category': item_data['category'],
                    'price': item_data['price'],
                    'description': item_data['description'],
                    'is_available': True,
                }
            )
            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'[OK] Successfully seeded {created} new food items! '
                f'({len(SAMPLE_ITEMS) - created} already existed)'
            )
        )
