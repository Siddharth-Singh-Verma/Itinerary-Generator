from django.core.management.base import BaseCommand
from itinerary.models import Temple, Pandit, LunchSpot, Booking
import random

class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Cleaning existing data...')
        Booking.objects.all().delete()
        Temple.objects.all().delete()
        Pandit.objects.all().delete()
        LunchSpot.objects.all().delete()

        self.stdout.write('Creating Temples...')
        temples_data = [
            ("Kashi Vishwanath", "Varanasi, Uttar Pradesh", 25.3109, 83.0107, "Lord Shiva"),
            ("Golden Temple", "Amritsar, Punjab", 31.6200, 74.8765, "Guru Granth Sahib"),
            ("Tirumala Venkateswara", "Tirupati, Andhra Pradesh", 13.6833, 79.3472, "Lord Vishnu"),
            ("Vaishno Devi", "Katra, Jammu and Kashmir", 33.0308, 74.9490, "Goddess Durga"),
            ("Siddhivinayak", "Mumbai, Maharashtra", 19.0169, 72.8304, "Lord Ganesha"),
            ("Somnath", "Prabhas Patan, Gujarat", 20.8880, 70.4010, "Lord Shiva"),
            ("Kedarnath", "Kedarnath, Uttarakhand", 30.7352, 79.0669, "Lord Shiva"),
            ("Badrinath", "Badrinath, Uttarakhand", 30.7447, 79.4911, "Lord Vishnu"),
            ("Jagannath", "Puri, Odisha", 19.8049, 85.8179, "Lord Jagannath"),
            ("Rameshwaram", "Rameswaram, Tamil Nadu", 9.2881, 79.3174, "Lord Shiva"),
            ("Dwarkadhish", "Dwarka, Gujarat", 22.2376, 68.9667, "Lord Krishna"),
            ("Amarnath", "Jammu and Kashmir", 34.2157, 75.5024, "Lord Shiva"),
            ("Meenakshi Amman", "Madurai, Tamil Nadu", 9.9195, 78.1193, "Goddess Parvati"),
            ("Virupaksha", "Hampi, Karnataka", 15.3350, 76.4600, "Lord Shiva"),
            ("Brihadeeswarar", "Thanjavur, Tamil Nadu", 10.7828, 79.1318, "Lord Shiva"),
            ("Konark Sun Temple", "Konark, Odisha", 19.8876, 86.0945, "Sun God"),
            ("Sanchi Stupa", "Sanchi, Madhya Pradesh", 23.4820, 77.7396, "Lord Buddha"),
            ("Akshardham", "New Delhi", 28.6127, 77.2773, "Swaminarayan"),
            ("Lotus Temple", "New Delhi", 28.5535, 77.2588, "Baha'i Faith"),
            ("Sai Baba Temple", "Shirdi, Maharashtra", 19.7668, 74.4762, "Sai Baba"),
        ]

        for i, (name, address, lat, lng, deity) in enumerate(temples_data):
            Temple.objects.create(
                name=name,
                address=address,
                latitude=lat,
                longitude=lng,
                deity=deity,
                image_url=f"https://picsum.photos/seed/temple{i}/800/600",
                description=f"A famous temple dedicated to {deity}."
            )

        self.stdout.write('Creating Pandits...')
        pandit_names = [
            "Pandit Sharma", "Acharya Gupta", "Shastri Ji", "Pandit Verma", "Swami Iyer",
            "Pandit Joshi", "Acharya Mishra", "Shastri Trivedi", "Pandit Desai", "Swami Nair",
            "Pandit Kulkarni", "Acharya Bhat", "Shastri Rao", "Pandit Singh", "Swami Reddy",
            "Pandit Mehta", "Acharya Patel", "Shastri Kumar", "Pandit Das", "Swami Krishnan"
        ]
        specializations = ["Vedic Rituals", "Astrology", "Katha", "Vastu Shastra", "Marriage Ceremonies"]

        for i, name in enumerate(pandit_names):
            Pandit.objects.create(
                name=name,
                years_of_experience=random.randint(5, 40),
                specialization=random.choice(specializations),
                image_url=f"https://picsum.photos/seed/pandit{i}/400/400",
                description=f"Experienced in {random.choice(specializations)} with deep knowledge of scriptures."
            )

        self.stdout.write('Creating Lunch Spots...')
        restaurant_names = [
            "Saravana Bhavan", "Haldiram's", "Bikanerwala", "MTR", "Karim's",
            "Paradise Biryani", "Indian Coffee House", "Chokhi Dhani", "Rajdhani Thali", "Sagar Ratna",
            "Murugan Idli Shop", "Tunday Kababi", "Bade Miya", "Kesar Da Dhaba", "Glenary's",
            "Britannia & Co.", "Peter Cat", "Mavalli Tiffin Room", "Vidyarthi Bhavan", "Gulati"
        ]
        cuisines = ["South Indian", "North Indian", "Rajasthani", "Mughlai", "Street Food"]

        for i, name in enumerate(restaurant_names):
            # Assigning random locations near some temples for variety, or just random spots in India
            # For simplicity, let's scatter them around central India or near major cities
            lat = 20.0 + random.uniform(-5, 5)
            lng = 78.0 + random.uniform(-5, 5)
            
            LunchSpot.objects.create(
                name=name,
                address="Famous Food Street",
                latitude=lat,
                longitude=lng,
                cuisine=random.choice(cuisines),
                price_range=random.choice(['$', '$$', '$$$']),
                image_url=f"https://picsum.photos/seed/food{i}/800/600",
                description=f"Famous for authentic {random.choice(cuisines)} cuisine."
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated database with 20 Temples, 20 Pandits, and 20 Lunch Spots.'))
