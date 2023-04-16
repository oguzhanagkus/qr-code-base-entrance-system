from django import forms
from django.forms import widgets
from django.core.validators import FileExtensionValidator

from entrance_system.models import Personnel, Department, Location, AccessPoint


class ImportForm(forms.Form):
    csv_file = forms.FileField(validators=[FileExtensionValidator(["csv"])])


class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ("national_id", "first_name", "last_name", "email", "department", "active")
        exclude = ("secret_token", " qr_code_data")
        widgets = {
            "national_id": widgets.NumberInput(attrs={"class": "form-control"}),
            "first_name": widgets.TextInput(attrs={"class": "form-control"}),
            "last_name": widgets.TextInput(attrs={"class": "form-control"}),
            "email": widgets.EmailInput(attrs={"class": "form-control"}),
            "department": widgets.Select(attrs={"class": "form-control"}),
            "active": widgets.CheckboxInput(attrs={"class": "form-control"}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = {"name"}
        exclude = None
        widgets = {
            "name": widgets.TextInput(attrs={"class": "form-control"}),
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = {"name", "qr_code_type", "active", "departments", "access_point"}
        exclude = {"last_activity", "api_token"}
        widgets = {
            "name": widgets.TextInput(attrs={"class": "form-control"}),
            "qr_code_type": widgets.Select(attrs={"class": "form-control"}),
            "active": widgets.CheckboxInput(attrs={"class": "form-control"}),
            "departments": widgets.SelectMultiple(attrs={"class": "form-control", "style": "height: 250px;"}),
            "access_point": widgets.Select(attrs={"class": "form-control"}),
        }


class AccessPointForm(forms.ModelForm):
    class Meta:
        model = AccessPoint
        fields = {"ssid", "password"}
        exclude = None
        widgets = {
            "ssid": widgets.TextInput(attrs={"class": "form-control"}),
            "password": widgets.PasswordInput(attrs={"class": "form-control"}, render_value=True),
        }


class SettingsForm(forms.Form):
    hes_api_url = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    hes_api_token = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email_host = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email_port = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))
    email_use_tls = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "form-control"}))
    email_user = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    email_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}, render_value=True))