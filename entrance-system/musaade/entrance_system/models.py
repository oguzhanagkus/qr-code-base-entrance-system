from django.db import models
from django.utils import timezone

from entrance_system import utils


class AccessPoint(models.Model):
    ssid = models.CharField(max_length=32, verbose_name="SSID")
    password = models.CharField(max_length=64, verbose_name="Password")

    def __str__(self):
        return self.ssid

    class Meta:
        verbose_name = "Access Point"
        verbose_name_plural = "Access Points"



class Department(models.Model):
    name = models.CharField(max_length=16, verbose_name="Name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'


class Location(models.Model):
    QR_CODE_TYPES = (
        ('1', 'Personnel'),
        ('2', 'HES'),
    )

    name = models.CharField(max_length=16, unique=True, verbose_name="Name")
    qr_code_type = models.CharField(max_length=16, choices=QR_CODE_TYPES, verbose_name="QR Code Type")
    last_activity = models.DateTimeField(default=None, null=True, verbose_name="Last Activity")
    active = models.BooleanField(default=True, verbose_name="Active")
    departments = models.ManyToManyField(Department, default=None, blank=True, verbose_name="Departments")
    access_point = models.ForeignKey(AccessPoint, on_delete=models.CASCADE, default=None, blank=False, verbose_name="Access Point")
    api_token = models.CharField(max_length=96, unique=True, default=utils.api_token, verbose_name="API Token")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'


class Personnel(models.Model):
    national_id = models.PositiveBigIntegerField(unique=True, verbose_name="National ID")
    first_name = models.CharField(max_length=16, verbose_name="First Name")
    last_name = models.CharField(max_length=16, verbose_name="Last Name")
    email = models.EmailField(max_length=64, unique=True, verbose_name="Email")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Department")
    last_activity = models.DateTimeField(default=None, null=True, verbose_name="Last Activity")
    active = models.BooleanField(default=True, verbose_name="Active")
    secret_token = models.CharField(max_length=16, unique=True, default=utils.secret_token, verbose_name="Secret Token")
    qr_code_data = models.CharField(max_length=128, unique=True, verbose_name="QR Code Data")

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        if not self.qr_code_data:
            self.generate_qr_code_data()
        super(Personnel, self).save(*args, **kwargs)

    def generate_qr_code_data(self):
        crypto = utils.Cryptographer(iv=self.secret_token.encode("utf-8"))
        data = str(self.national_id) + "|" + self.first_name + "_" + self.last_name
        self.qr_code_data = crypto.encrypt(data).decode("utf-8")

    @classmethod
    def get_printable_column_names(cls):
        return [
            cls._meta.get_field("national_id").verbose_name,
            cls._meta.get_field("first_name").verbose_name,
            cls._meta.get_field("last_name").verbose_name,
            cls._meta.get_field("email").verbose_name,
            cls._meta.get_field("department").verbose_name,
            cls._meta.get_field("last_activity").verbose_name,
            cls._meta.get_field("active").verbose_name
        ]

    def get_printable_data(self):
        return [
            self.national_id, self.first_name, self.last_name,
            self.email, self.department, self.last_activity, self.active
        ]

    class Meta:
        verbose_name = 'Personnel'
        verbose_name_plural = 'Personnel'





class PersonnelActivity(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=1, verbose_name="Personnel")
    time = models.DateTimeField(default=timezone.now, verbose_name="Time")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1, verbose_name="Location")
    result = models.BooleanField(default=False, verbose_name="Result")
    message = models.CharField(max_length=256, default="", verbose_name="Message")

    def __str__(self):
        return "{} {}".format(self.personnel.first_name, self.personnel.last_name)

    @classmethod
    def get_printable_column_names(cls):
        return [
            cls._meta.get_field("personnel").verbose_name,
            cls._meta.get_field("time").verbose_name,
            cls._meta.get_field("location").verbose_name,
            cls._meta.get_field("result").verbose_name,
            cls._meta.get_field("message").verbose_name,
        ]

    def get_printable_data(self):
        return [self.personnel, self.time, self.location, self.result, self.message]

    class Meta:
        verbose_name = 'Personnel Activity'
        verbose_name_plural = 'Personnel Activity'


class HESActivity(models.Model):
    first_name = models.CharField(max_length=16, verbose_name="First Name")
    last_name = models.CharField(max_length=16, verbose_name="Last Name")
    time = models.DateTimeField(default=timezone.now, verbose_name="Time")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1, verbose_name="Location")
    result = models.BooleanField(default=False, verbose_name="Result")

    class Meta:
        verbose_name = 'HES Activity'
        verbose_name_plural = 'HES Activity'

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    @classmethod
    def get_printable_column_names(cls):
        return [
            "Person",
            cls._meta.get_field("time").verbose_name,
            cls._meta.get_field("location").verbose_name,
            cls._meta.get_field("result").verbose_name,
        ]

    def get_printable_data(self):
        return ["{}{}".format(self.first_name, self.last_name), self.time, self.location, self.result]

    class Meta:
        verbose_name = 'HES Activity'
        verbose_name_plural = 'HES Activity'
