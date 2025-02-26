import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings")  # Replace "myproject" with your project folder name
django.setup()

# Now you can import your models
from content.models import Guitar
import json

# Load JSON file
with open("guitars.json", encoding="utf-8") as file:
    data = json.load(file)

# Insert each item into the database
for item in data:
    Guitar.objects.create(
        brand=item["brand"],
        pickups=item["pickups"],
        model=item["model"],
        price=item["price"].replace(",-", "").replace(" ", ""),  # Clean price
        image=item["image"],
        description=item["description"],
        shape=item["shape"]
    )

print("Data successfully imported!")
