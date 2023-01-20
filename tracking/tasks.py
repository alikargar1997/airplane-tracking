import json

from celery import shared_task, task
from django.core.cache import cache
from django.core.mail import send_mail
from django_celery_beat.models import PeriodicTask

from tracking.utils import Comparator, convert_datetime, disable_scheduler

from . import models


@shared_task(name="tracking")
def tracking(username: str, flight_number: str, user_email: str):
    """Main logic for check airplane status and notify user by changes of the status in the interval

    Args:
        username ([str]): username of own user
        flight_number ([str]): flight number of the flight
        user_email ([str]): email of the user
    """
    # gets last flight status crawled from database
    current_flight_status = models.FlightStatus.objects.get_latest_by_flight_number(
        flight_number
    )
    if not current_flight_status.exists():
        return
    current_flight_status = current_flight_status.first()
    cacheKey = username + "-" + flight_number
    # Gets the last flight status sent to the user
    last_status_sent_pk = cache.get(cacheKey)
    # Checks if both current status and last status are the same
    if current_flight_status.pk == last_status_sent_pk:
        pt = PeriodicTask.objects.filter(name=flight_number)
        if pt.exists():
            # Check if crawling of the flight statuses done
            if pt.first().enabled == False:
                # Disable the user flight tracking scheduler
                disable_scheduler(cacheKey)
                flight_user = models.FlightUser.objects.get_by_flight_number(
                    username=username, flight_number=flight_number
                )
                if flight_user.exists():
                    flight_user = flight_user.first()
                    # Set the status of tracking to false
                    flight_user.status = False
                    flight_user.save()
    # Check if the last flight status that sent to user exists
    if isinstance(last_status_sent_pk, int):
        last_status_sent = models.FlightStatus.objects.filter(pk=last_status_sent_pk)
        if last_status_sent.exists():
            last_status_sent = last_status_sent.first()
            # Compare 2 status of flight ,last status sent and the current status of flight
            comparator = Comparator(current_flight_status, last_status_sent)
            # Notify user if there is any changes
            if comparator.compare_arrival_time() or comparator.compare_distance():
                mail_user(username, comparator, user_email, False)
            # Set the current status as last status sent
            cache.set(cacheKey, current_flight_status.pk)
            return
    # Calculate some params of current flight status
    # Here is the first time that user starts tracking
    comparator = Comparator(current_flight_status, None)
    mail_user(username, comparator, user_email, True)
    # Set the current status as last status sent
    cache.set(cacheKey, current_flight_status.pk)


@task
def mail_user(username, comparator_obj, user_email, is_first):
    """Send email to user

    Args:
        username ([str]): username of own user
        comparator_obj ([Object]): an instance of Comparator class
        user_email ([str]): email of own user
        is_first (bool): check if its first email that is sending to user or not
    """
    if is_first:
        message = """
            Hi dear {0} \n  
            Last status of airplane {1} : \n
            Time of Arrival: {2} \n
            Current Location: {3}
            """.format(
            username,
            comparator_obj.flight_number,
            comparator_obj.arrival_time,
            comparator_obj.current_location,
        )
    else:
        message = """
            Hi dear {0} \n

            New update of airplane {1} status: \n 

            Time of Arrival: {2} ({3} hours delay)\n
            Location: changed from {4} to {5}
            """.format(
            username,
            comparator_obj.flight_number,
            comparator_obj.arrival_time,
            comparator_obj._find_arrival_time_delay(),
            comparator_obj.last_location,
            comparator_obj.current_location,
        )

    send_mail(
        "Package Tracking from Airplane monitoring App",
        message,
        "ali.kargar.p@gmail.com",
        (user_email,),
    )


@shared_task(name="crawler")
def crawler(filepath, flight_number):
    """Crawler

    Args:
        filepath ([sre]): path of the file of crawling data
        flight_number ([str]): flight number
    """
    cleaned_data = dict()
    with open(filepath, mode="r") as f:
        position = 0
        # Get the last flight status t
        queryset = (
            models.FlightStatus.objects.filter(flight__flight_number=flight_number)
            .select_related("flight")
            .order_by("-date")
        )
        if queryset.exists():
            # calculate last crawled data
            position = queryset[0].position + 1
        json_obj = json.load(f)
        data_list = json_obj["data"]
        # Check if the last crawled data is not the last crawl
        if position > data_list.__len__() - 1:
            f.close()
            # Disable the crawler for this flile
            disable_scheduler(flight_number)
            return
        data = data_list[position]
        cleaned_data["position"] = position
        cleaned_data["latitude"] = data["coordinates"]["latitude"]
        cleaned_data["longitude"] = data["coordinates"]["longitude"]
        cleaned_data["flight_id"] = models.Flight.objects.get(
            flight_number=flight_number
        ).pk
        cleaned_data["arrival_time"] = convert_datetime(data["arrival_time"])
        models.FlightStatus.objects.create(**cleaned_data)
    return
