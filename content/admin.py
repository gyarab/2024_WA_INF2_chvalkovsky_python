from django.contrib import admin
from .models import Guitar, Brand, Genre

# Register your models here.

admin.site.register(Guitar)
admin.site.register(Brand)
admin.site.register(Genre)