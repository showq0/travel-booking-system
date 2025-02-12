from django import forms
from bookings.models import Booking
from bookings.constants import hotel_details_schema
from django_jsonform.validators import JSONSchemaValidator, JSONSchemaValidationError
import json
from django_jsonform.forms.fields import JSONFormField


class BookingForm(forms.ModelForm):
    hotel_details = JSONFormField(schema={})

    class Meta:
        model = Booking
        fields = ('user', 'travel_package','hotel_details','status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        temp_data = None
        self.fields['hotel_details'].widget.schema = hotel_details_schema

        if self.instance and self.instance.pk:
            temp_data = self.instance.hotel_details

        if temp_data:
            try:
                validator = JSONSchemaValidator(hotel_details_schema)
                validator(temp_data)
            except JSONSchemaValidationError as e:
                self.fields['hotel_details'].help_text += (
                        "<p style='color:#B00020;'> <strong>" + ", ".join(e.messages) + " || the data is" + json.dumps(temp_data) + "</strong>:</p>"
                )
