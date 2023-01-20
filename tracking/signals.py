from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask

from tracking import models, tasks
from tracking.utils import update_or_create_scheduler


@receiver(post_save, sender=models.Flight)
def create_flight(sender, instance, created, **kwargs):
    """Update or Creates a crawling task and schedule it"""
    if created:
        update_or_create_scheduler(
            instance.schedule_delay,
            instance.flight_number,
            "crawler",
            {
                "filepath": instance.informations_file.path,
                "flight_number": instance.flight_number,
            },
        )


@receiver(post_save, sender=models.FlightUser, dispatch_uid="handle_scheduler")
def create_flight_user(sender, instance, created, **kwargs):
    """Update,Create or disable tracking scheduler after any changes to FlightUser model"""
    flight_number = instance.flight.flight_number
    username = instance.user.username
    if instance.status:
        update_or_create_scheduler(
            instance.schedule_delay,
            username + "-" + flight_number,
            "tracking",
            {
                "username": username,
                "flight_number": flight_number,
                "user_email": instance.user.email,
            },
        )
    else:
        tasks.disable_scheduler(username + "-" + flight_number)


@receiver(pre_delete, sender=models.Flight, dispatch_uid="handle_scheduler")
def delete_periodic_task_by_flight(sender, instance, **kwargs):
    """Removes the periodic tasks referes to the flights after deleting flights"""
    PeriodicTask.objects.filter(name__contains=instance.flight_number).delete()


@receiver(pre_delete, sender=models.FlightUser, dispatch_uid="handle_scheduler")
def delete_periodic_task_by_flight(sender, instance, **kwargs):
    """Removes the periodic tasks referes to the flights after deleting flights"""
    PeriodicTask.objects.filter(
        name=instance.user.username + "-" + instance.flight.flight_number
    ).delete()
