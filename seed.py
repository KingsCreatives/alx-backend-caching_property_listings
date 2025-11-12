import os
import django
import random
from decimal import Decimal
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_caching_property_listings.settings')
django.setup()

from properties.models import Property

# Initialize Faker
fake = Faker()

def seed_properties(n=1000):
    properties = []
    for _ in range(n):
        title = fake.sentence(nb_words=4)
        description = fake.paragraph(nb_sentences=5)
        price = round(Decimal(random.uniform(50000, 1000000)), 2)  
        location = fake.city()
        
        properties.append(Property(
            title=title,
            description=description,
            price=price,
            location=location
        ))

    Property.objects.bulk_create(properties)
    print(f"✅ Successfully added {n} properties to the database.")

if __name__ == "__main__":
    print("🌱 Seeding database with fake property data...")
    Property.objects.all().delete() 
    seed_properties(1000)
    print("🎉 Seeding complete!")
