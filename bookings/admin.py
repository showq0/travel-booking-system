from django.contrib import admin
from bookings.models import Booking, TravelPackage
from bookings.forms import BookingForm
# Register your models here.


class BookingAdmin(admin.ModelAdmin):
    form = BookingForm


admin.site.register(Booking, BookingAdmin)
admin.site.register(TravelPackage)

