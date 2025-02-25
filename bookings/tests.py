from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from bookings.models import Booking, User, TravelPackage, STATUS_CHOICES


class BookingTests(TestCase):
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username="testuser", password="password")
        self.travel_package = TravelPackage.objects.create(
            destination="Paris",
            price=1200.50,
            available_slot=20,
            travel_date="2025-06-15"
        )

    def test_create_bookings(self):
        booking = Booking(user=self.user, travel_package=self.travel_package, status=STATUS_CHOICES[1][0],
                    hotel_details={"room": "101"})

        booking.save()
        travel_package = TravelPackage.objects.get(pk=self.travel_package.pk)

        self.assertEqual(travel_package.available_slot, 19)

    def test_delete_bookings(self):
        booking = Booking(user=self.user, travel_package=self.travel_package, status=STATUS_CHOICES[1][0],
                          hotel_details={"room": "101"})

        booking.save()
        booking.delete()
        travel_package = TravelPackage.objects.get(pk=self.travel_package.pk)
        self.assertEqual(travel_package.available_slot, 20)
