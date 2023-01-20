from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.db import models
from django.shortcuts import reverse


class CustomUserQuerySet(models.QuerySet):
    def user_by_email(self, email: str) -> models.QuerySet:
        return self.get(email=email)


class CustomUserManager(BaseUserManager):
    def get_queryset(self):
        return CustomUserQuerySet(self.model, using=self._db)

    def get_by_email(self, email: str) -> models.QuerySet:
        return self.get_queryset().user_by_email(email)


class CustomUser(AbstractUser):
    """Updated user object with new params and methods

    Args:
        AbstractUser ([obj]): inherit the Abstractuser class

    """

    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    email = models.EmailField(unique=True)
    objects = CustomUserManager

    def __str__(self):
        """model objects displaying names

        Returns:
            [str]: user email
        """
        return self.email

    def get_absolute_url(self):
        return reverse("accounts:signin")
