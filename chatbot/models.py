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