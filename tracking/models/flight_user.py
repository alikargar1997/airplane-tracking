from django.core.validators import MinValueValidator
from django.db import models
from django.shortcuts import reverse

from accounts.models import CustomUser
from tracking.models import Flight


class FlightUserQuerySet(models.QuerySet):
    def flight_user_by_flight_number(
        self, username: str, flight_number: str
    ) -> models.QuerySet:
        return self.filter(user__username=username, flight__flight_number=flight_number)

    def by_user(self, user: CustomUser) -> models.QuerySet:
        return self.filter(user=user).order_by("-status")


class FlightUserManager(models.Manager):
    def get_queryset(self):
        return FlightUserQuerySet(self.model, using=self._db).select_related(
            "user", "flight"
        )

    def get_by_flight_number(
        self, username: str, flight_number: str
    ) -> models.QuerySet:
        return self.get_queryset().flight_user_by_flight_number(username, flight_number)

    def get_by_user(self, user: CustomUser) -> models.QuerySet:
        return self.get_queryset().by_user(user)


class FlightUser(models.Model):
    """Flight's users through model to create connection between users and flights"""

    user = models.ForeignKey(
        CustomUser, related_name="user_flights", on_delete=models.CASCADE
    )
    flight = models.ForeignKey(
        Flight, related_name="flight_users", on_delete=models.CASCADE
    )
    status = models.BooleanField(default=False)
    schedule_delay = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)]
    )
    objects = FlightUserManager

    class Meta:
        unique_together = ("user", "flight")

    def get_absolute_url(self):
        return reverse("tracking:list_tracking")

    def __str__(self):
        return self.user.username + "," + self.flight.flight_number
