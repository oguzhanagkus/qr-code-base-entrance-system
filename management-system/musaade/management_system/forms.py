from django import forms
from django.forms import widgets

from management_system.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("company_name", "person_name", "email", "hardware_count")
        exclude = ()
        widgets = {
            "company_name": widgets.TextInput(attrs={"class": "form-control"}),
            "person_name": widgets.TextInput(attrs={"class": "form-control"}),
            "email": widgets.EmailInput(attrs={"class": "form-control"}),
            "hardware_count": widgets.NumberInput(attrs={"class": "form-control"}),
        }
