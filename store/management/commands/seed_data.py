"""Management command to populate the database with sample food items."""

from django.core.management.base import BaseCommand
from store.models import FoodItem


SAMPLE_ITEMS = [
    # Starters
    {'name': 'Veg Spring Rolls', 'category': 'starters', 'price': 149, 'description': 'Crispy rolls stuffed with fresh vegetables and served with sweet chilli dip.'},
    {'name': 'Chicken Tikka', 'category': 'starters', 'price': 249, 'description': 'Tender chicken marinated in yogurt and spices, grilled to perfection.'},
    {'name': 'Paneer Tikka', 'category': 'starters', 'price': 219, 'description': 'Soft cottage cheese cubes marinated in spiced yogurt, chargrilled.'},
    {'name': 'Garlic Mushrooms', 'category': 'starters', 'price': 179, 'description': 'Button mushrooms sautéed in garlic butter with fresh herbs.'},

    # Main Course
    {'name': 'Butter Chicken', 'category': 'main_course', 'price': 299, 'description': 'Succulent chicken in rich, creamy tomato-based gravy with butter.'},
    {'name': 'Dal Makhani', 'category': 'main_course', 'price': 229, 'description': 'Slow-cooked black lentils in a buttery, creamy tomato gravy.'},
    {'name': 'Paneer Butter Masala', 'category': 'main_course', 'price': 269, 'description': 'Soft paneer cubes in a velvety, mildly spiced tomato-cashew gravy.'},
    {'name': 'Chicken Biryani', 'category': 'main_course', 'price': 349, 'description': 'Fragrant basmati rice layered with spiced chicken and caramelised onions.'},
    {'name': 'Palak Paneer', 'category': 'main_course', 'price': 239, 'description': 'Cottage cheese in a smooth, freshly pureed spinach gravy.'},
    {'name': 'Mutton Rogan Josh', 'category': 'main_course', 'price': 389, 'description': 'Slow-braised mutton in aromatic Kashmiri spices and deep red gravy.'},

    # Snacks
    {'name': 'Samosa (2 pcs)', 'category': 'snacks', 'price': 49, 'description': 'Crispy pastry triangles stuffed with spiced potatoes and peas.'},
    {'name': 'Aloo Tikki', 'category': 'snacks', 'price': 79, 'description': 'Golden potato patties with chutneys and sev.'},
    {'name': 'Pav Bhaji', 'category': 'snacks', 'price': 129, 'description': 'Spiced mixed vegetable mash served with buttered pav rolls.'},
    {'name': 'French Fries', 'category': 'snacks', 'price': 99, 'description': 'Golden, crispy fries served with ketchup and mayo.'},

    # Desserts
    {'name': 'Gulab Jamun', 'category': 'desserts', 'price': 89, 'description': 'Soft milk-solid dumplings soaked in rose-scented sugar syrup.'},
    {'name': 'Chocolate Brownie', 'category': 'desserts', 'price': 129, 'description': 'Rich, fudgy chocolate brownie served warm with a scoop of vanilla ice cream.'},
    {'name': 'Mango Kulfi', 'category': 'desserts', 'price': 99, 'description': 'Dense, creamy traditional Indian ice cream with alphonso mango.'},
    {'name': 'Rasgulla', 'category': 'desserts', 'price': 79, 'description': 'Light, spongy cheese balls in a light sugar syrup.'},

    # Beverages
    {'name': 'Mango Lassi', 'category': 'beverages', 'price': 89, 'description': 'Chilled yogurt drink blended with sweet Alphonso mango.'},
    {'name': 'Masala Chai', 'category': 'beverages', 'price': 49, 'description': 'Spiced Indian tea brewed with ginger, cardamom, and milk.'},
    {'name': 'Fresh Lime Soda', 'category': 'beverages', 'price': 59, 'description': 'Refreshing chilled lime juice topped with sparkling soda.'},
    {'name': 'Cold Coffee', 'category': 'beverages', 'price': 119, 'description': 'Blended iced coffee with milk and a hint of vanilla.'},
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
