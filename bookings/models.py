from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date

PENDING = 'pending'
CONFIRMED = 'confirmed'
CANCELLED = 'cancelled'
COMPLETED = 'completed'

STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (CONFIRMED, 'Confirmed'),
    (CANCELLED, 'Cancelled'),
    (COMPLETED, 'Completed'),
]


def validate_travel_date(value):
    if value < date.today():
        raise ValidationError("Travel date cannot be in the past.")


class TravelPackage (models.Model):
    destination = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_slot = models.IntegerField(validators=[MaxValueValidator(440)])
    travel_date = models.DateField(validators=[validate_travel_date])

    def __str__(self):
        return self.destination

    def get_absolute_url(self):
        return reverse('travel_package_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    travel_package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING)
    hotel_details = models.JSONField(default={})

    class Meta:
        unique_together = ['user', 'travel_package']

    def __str__(self):
        return f'Booking by {self.user} for {self.travel_package}'

    def get_absolute_url(self):
        return reverse("booking_details", args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

