from django.db import models

# Create your models here.
class Guitar(models.Model):
    brand = models.CharField(max_length=20, blank=False, null=False)
    pickups = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=100, blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)
    image = models.URLField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    shape = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return f"{self.brand} {self.model}"