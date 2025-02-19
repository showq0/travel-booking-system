from django import forms
from bookings.models import Booking, JSONSchema
from bookings.constants import SchemaCodes
from django_jsonform.validators import JSONSchemaValidator, JSONSchemaValidationError
import json
from django_jsonform.forms.fields import JSONFormField


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
            schema_obj = JSONSchema.objects.filter(name=SchemaCodes.hotel_details_schema).last()
            if schema_obj:
                schema = schema_obj.schema

        if temp_data is not None:
            try:
                schema_obj = JSONSchema.objects.get(name=SchemaCodes.hotel_details_schema,
                                                    version=self.instance.hotel_details_schema_version)
                schema = schema_obj.schema

                validator = JSONSchemaValidator(schema)
                validator(temp_data)
            except JSONSchema.DoesNotExist as e:
                self.fields['hotel_details'].help_text += (
                        "<p style='color:#B00020;'> <strong> this form doesnt exist "
                        " || the data is" + json.dumps(temp_data) + "</strong>:</p>"
                )
            except JSONSchemaValidationError as e:
                self.fields['hotel_details'].help_text += (
                        "<p style='color:#B00020;'> <strong>" + ", ".join(e.messages) +
                        " || the data is" + json.dumps(temp_data) + "</strong>:</p>"
                )

        self.fields['hotel_details'].widget.schema = schema

    def save(self, commit=True):
        super().clean()
        instance = super().save(commit=False)

        if instance.pk is None:  # create new object
            schema_obj = JSONSchema.objects.filter(name=SchemaCodes.hotel_details_schema).last()
            instance.hotel_details_schema_version = schema_obj.version

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
