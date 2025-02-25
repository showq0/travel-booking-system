from django.db import models, transaction
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date
from bookings.constants import SchemaCodes

PENDING = 'pending'
CONFIRMED = 'confirmed'
CANCELLED = 'cancelled'

STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (CONFIRMED, 'Confirmed'),
    (CANCELLED, 'Cancelled'),
]


def validate_travel_date(value):
    if value < date.today():
        raise ValidationError("Travel date cannot be in the past.")


class TravelPackage(models.Model):
    destination = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_slot = models.IntegerField(
        validators=[MaxValueValidator(440), MinValueValidator(0, message="There is no seat available.")], )
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
    hotel_details_schema_version = models.IntegerField(default=1)

    class Meta:
        unique_together = ['user', 'travel_package']

    def __str__(self):
        return f'Booking by {self.user} for {self.travel_package}'

    def get_absolute_url(self):
        return reverse("booking_details", args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.full_clean()
        is_new = self.pk is None

        book_seat = 0

        with transaction.atomic():

            if is_new and self.status == CONFIRMED:
                book_seat -= 1
            elif not is_new:
                old_booking = Booking.objects.get(pk=self.pk)

                if old_booking.status != CONFIRMED and self.status == CONFIRMED:
                    book_seat -= 1
                elif old_booking.status == CONFIRMED and self.status != CONFIRMED:
                    book_seat += 1
            # Update the available_slot only if necessary
            if book_seat != 0:
                # lock travel_package
                travel_package = TravelPackage.objects.select_for_update().get(pk=self.travel_package.pk)
                travel_package.available_slot += book_seat
                travel_package.save(update_fields=["available_slot"])

            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Restore slot when a booking is deleted only if confirmed
        with transaction.atomic():
            if self.status == CONFIRMED:
                travel_package = TravelPackage.objects.select_for_update().get(pk=self.travel_package.pk)
                travel_package.available_slot += 1
                travel_package.save()

            super().delete(*args, **kwargs)


class JSONSchema(models.Model):
    name = models.CharField(choices=SchemaCodes.choices, max_length=50)
    version = models.AutoField(primary_key=True)
    schema = models.JSONField(default={})

    class Meta:
        unique_together = ['version', 'name']
