from django.shortcuts import render
from django.views.generic import ListView
from bookings.models import Booking, TravelPackage
# Create your views here.


class BookingListView(ListView):
    model = Booking
    template_name = 'booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(id=self.kwargs['id'])


class TravelPackageListView(ListView):
    model = TravelPackage
    template_name = 'travel_package_list.html'
    context_object_name = 'travel_packages'

    def get_queryset(self):
        return TravelPackage.objects.filter(id=self.kwargs['id'])