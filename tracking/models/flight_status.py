from django.db import models

from tracking.models import Flight


class FlightStatusQuerySet(models.QuerySet):
    def latest_flight_status_by_flight_number(
        self, flight_number: str
    ) -> models.QuerySet:
        return self.filter(flight__flight_number=flight_number).order_by("-date")


class FlightStatusManager(models.Manager):
    """Custom Flight Status manager"""

    def get_queryset(self):
        return FlightStatusQuerySet(self.model, using=self._db).select_related("flight")

    def get_latest_by_flight_number(self, flight_number: str) -> models.QuerySet:
        return self.get_queryset().latest_flight_status_by_flight_number(flight_number)

    def create(self, *args, **kwargs):
        """FlightStatus create manager customized to count and save the position of object in the crawled objects"""
        if "position" not in kwargs:
            queryset = self.filter(
                flight__flight_number=kwargs["flight_number"]
            ).order_by("-date")
            if queryset.exists():
                position = queryset[0].position + 1
                kwargs["position"] = position
        return super(FlightStatusManager, self).create(*args, **kwargs)


class FlightStatus(models.Model):
    """Status of flight resulted by crawler"""

    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    longitude = models.DecimalField(max_digits=6, decimal_places=3)
    latitude = models.DecimalField(max_digits=6, decimal_places=3)
    arrival_time = models.DateTimeField(auto_now_add=False)

    objects = FlightStatusManager

    def __str__(self):
        return self.flight.flight_number + " - " + str(self.position)
