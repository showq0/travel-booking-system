from django.urls import path
from bookings.views import BookingListView, TravelPackageListView

urlpatterns = [
    path('booking-details/<int:id>/', BookingListView.as_view(), name='booking_details'),
    path('travel-package-details/<int:id>/', TravelPackageListView.as_view(), name='travel_package_details'),]
