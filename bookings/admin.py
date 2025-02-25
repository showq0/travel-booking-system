from django.contrib import admin
from bookings.models import Booking, TravelPackage, JSONSchema
from bookings.forms import BookingForm
# Register your models here.


class BookingAdmin(admin.ModelAdmin):
    form = BookingForm

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


admin.site.register(Booking, BookingAdmin)
admin.site.register(TravelPackage)
admin.site.register(JSONSchema)


