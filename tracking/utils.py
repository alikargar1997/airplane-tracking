import json
from dataclasses import dataclass
from datetime import datetime
from math import atan2, cos, radians, sin, sqrt

import pytz
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from tracking.models import FlightStatus


@dataclass
class Comparator:
    """Compare 2 status of the user's flight,extracts the formatted values of the objects"""

    current_flight_status: FlightStatus
    last_flight_status: FlightStatus

    def compare_arrival_time(self):
        """Compares arrival time of flights

        Returns:
            [bool]: True if there is a differ between the objects and False otherwise
        """
        if (
            self.last_flight_status.arrival_time
            != self.current_flight_status.arrival_time
        ):
            return True
        return False

    def compare_distance(self):
        """Compares distance between 2 statuses

        Returns:
            [type]: True if distance is more than 200km, False otherwise
        """
        if self._find_distance() > 200:
            return True
        return False

    def _find_arrival_time_delay(self):
        """Find differ between arrival time of last status and current

        Returns:
            [decimal]: the difference
        """
        return "{:.2f}".format(
            (
                self.current_flight_status.arrival_time
                - self.last_flight_status.arrival_time
            ).total_seconds()
            / 3600
        )

    def _find_distance(self):
        """Finding the distance of 2 statuses in km.

        Returns:
            [float]: distance
        """
        R = 6373.0
        lat1 = radians(self.current_flight_status.latitude)
        lon1 = radians(self.current_flight_status.longitude)
        lat2 = radians(self.last_flight_status.latitude)
        lon2 = radians(self.last_flight_status.longitude)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    @property
    def current_location(self):
        """Cuttrnt location of the flight in specific format

        Returns:
            [str]: current loc
        """
        return str(
            [
                str(self.current_flight_status.latitude),
                str(self.current_flight_status.longitude),
            ]
        )

    @property
    def last_location(self):
        """last location of the flight sent before in specific format
        Returns:
            [str]: last loc
        """
        return str(
            [
                str(self.last_flight_status.latitude),
                str(self.last_flight_status.longitude),
            ]
        )

    @property
    def flight_number(self):
        """Flight number of the flight

        Returns:
            [type]: [description]
        """
        return self.current_flight_status.flight.flight_number

    @property
    def arrival_time(self):
        """Time of arrival in specific fornat

        Returns:
            [type]: [description]
        """
        return self.current_flight_status.arrival_time.strftime("%d %B %Y, %I:%M %p")


def convert_datetime(timestamp: int) -> datetime:
    """Convert the timestamp to normal datetime object

    Args:
        timestamp ([int]):timestamp

    Returns:
        [obj]: datetime object
    """
    local_tz = pytz.timezone("Asia/Tehran")
    utc_dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    return local_tz.normalize(utc_dt.astimezone(local_tz))


def disable_scheduler(name: str):
    """Disable the scheduled task by the name

    Args:
        name ([str]): name of PeriodicTask
    """
    pt = PeriodicTask.objects.filter(name=name)
    if pt.exists():
        ps_obj = pt.first()
        # Disable the scheduler
        ps_obj.enabled = False
        ps_obj.save()


def update_or_create_scheduler(delay, name, task, kwargs):
    """update or create the PeriodicTask scheduler

    Args:
        delay ([int]): delay of the task for schedule
        name ([str]): name of PeriodicTask
        task ([str]): task name in str
        kwargs ([dict]): dictionary needed for the task
    """
    # Get or Creates an interval
    schedule = IntervalSchedule.objects.filter(
        every=delay, period=IntervalSchedule.MINUTES
    )
    if schedule.exists():
        schedule = schedule.first()
    else:
        schedule = IntervalSchedule.objects.create(
            every=delay, period=IntervalSchedule.MINUTES
        )

    # Create or update the PeriodicTask for scheduling and activating
    try:
        periodic_task = PeriodicTask.objects.get(name=name)
        periodic_task.interval = schedule
        periodic_task.task = task
        periodic_task.kwargs = json.dumps(kwargs)
        periodic_task.enabled = True
        periodic_task.save()
    except PeriodicTask.DoesNotExist:
        periodic_task = PeriodicTask.objects.create(
            interval=schedule,
            name=name,
            task=task,
            kwargs=json.dumps(kwargs),
            enabled=True,
        )
