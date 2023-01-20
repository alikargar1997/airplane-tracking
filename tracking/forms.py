from django import forms

from tracking import models


class Tracking(forms.ModelForm):
    """Airplane Tracking adding form"""

    class Meta:
        model = models.FlightUser
        fields = ("flight", "schedule_delay")
        widgets = {"flight": forms.Select()}
        help_texts = {"schedule_delay": "In minutes"}
