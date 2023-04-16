from django.db import models

from management_system import utils


class Customer(models.Model):
    company_name = models.CharField(max_length=32, unique=True, verbose_name="Company Name")
    person_name = models.CharField(max_length=32, unique=True, verbose_name="Person")
    email = models.EmailField(max_length=64, unique=True, verbose_name="Email")
    hardware_count = models.PositiveIntegerField(verbose_name="Hardware Count", default=0)
    ip_address = models.CharField(max_length=32, verbose_name="IP Address", default="")
    uuid = models.CharField(max_length=64, unique=True, verbose_name="Person", default=utils.generate_uuid)

    def __str__(self):
        return self.company_name
