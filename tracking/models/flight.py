from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.validators import MinValueValidator
from django.db import models

from accounts.models import CustomUser


class Flight(models.Model):
    """Flights informations model"""

    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    flight_number = models.CharField(max_length=200, unique=True)
    airline = models.CharField(max_length=200)
    schedule_delay = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)]
    )
    informations_file = models.FileField(
        storage=FileSystemStorage(location=settings.MEDIA_ROOT),
        upload_to="flights_info",
        default="flights_info/crawler_result.json",
    )
    users = models.ManyToManyField(
        CustomUser, through="FlightUser", related_name="flights", symmetrical=False
    )

    def __str__(self):
        return self.flight_number
