from django.contrib import admin

from . import models

# Register your models here.


admin.site.register(models.Flight)
admin.site.register(models.FlightStatus)
admin.site.register(models.FlightUser)
