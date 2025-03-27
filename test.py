import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings")
django.setup()

from content.models import Guitar
import json

with open("guitars.json", encoding="utf-8") as file:
    data = json.load(file)

for item in data:
    Guitar.objects.create(
        brand=item["brand"],
        pickups=item["pickups"],
        model=item["model"],
        price=item["price"].replace(",-", "").replace(" ", ""),
        image=item["image"],
        description=item["description"],
        shape=item["shape"]
    )

print("Data successfully imported!")
