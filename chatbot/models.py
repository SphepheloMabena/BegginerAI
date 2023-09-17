from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class FuelPrice(models.Model):
    FUEL_TYPE_CHOICES = (
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
    )

    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPE_CHOICES)
    litres_price = models.CharField(max_length=50)
    gallons_price = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fuel_type} - {self.litres_price} / {self.gallons_price}"


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    user_message = models.TextField()
    bot_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)