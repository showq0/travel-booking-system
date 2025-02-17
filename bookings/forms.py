from django import forms
from bookings.models import Booking,JSONSchema
from bookings.constants import SchemaCodes
from django_jsonform.validators import JSONSchemaValidator, JSONSchemaValidationError
import json
from django_jsonform.forms.fields import JSONFormField
# from jsoneditor.forms import JSONEditor


class BookingForm(forms.ModelForm):
    hotel_details = JSONFormField(schema={})

    class Meta:
        model = Booking
        fields = ('user', 'travel_package', 'hotel_details', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        temp_data = None
        schema = {
            "type": "object",
            "properties": {},
        }
        if self.instance and self.instance.pk:
            temp_data = self.instance.hotel_details

        if temp_data is None:
            schema = JSONSchema.objects.filter(
                name=SchemaCodes.hotel_details_schema).last().schema

        if temp_data is not None:
            schema = JSONSchema.objects.get(
                name=SchemaCodes.hotel_details_schema, version=self.instance.hotel_details_schema_version).schema
            try:
                validator = JSONSchemaValidator(schema)
                validator(temp_data)
            except JSONSchemaValidationError as e:
                self.fields['hotel_details'].help_text += (
                        "<p style='color:#B00020;'> <strong>" + ", ".join(e.messages) + " || the data is" + json.dumps(temp_data) + "</strong>:</p>"
                )

        self.fields['hotel_details'].widget.schema = schema

    def save(self, commit=True):
        super().clean()
        instance = super().save(commit=False)

        instance.hotel_details_schema_version = JSONSchema.objects.filter(
                name=SchemaCodes.hotel_details_schema).last().version

        if commit:
            instance.save()
        return instance

# class JsonSchemasForm(forms.ModelForm):
#     name = forms.ChoiceField(choices=[], required=True)
#     schema = forms.JSONField(widget=JSONEditor)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['form_code'].choices = FormCodes.choices
#
#     class Meta:
#         model = JSONSchema
#         fields = '__all__'
