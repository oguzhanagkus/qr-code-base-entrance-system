from django.contrib import admin

from entrance_system.models import AccessPoint, Personnel, Department, Location, PersonnelActivity, HESActivity

admin.site.register(AccessPoint)
admin.site.register(Personnel)
admin.site.register(Department)
admin.site.register(Location)
admin.site.register(PersonnelActivity)
admin.site.register(HESActivity)
