from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, View

from . import forms, models


class TrackingCreateView(LoginRequiredMixin, CreateView):
    """Create a tracking scheduler task"""

    form_class = forms.Tracking
    template_name = "tracking/create.html"

    def form_valid(self, form):
        flight_user = models.FlightUser.objects.filter(
            user=self.request.user, flight=form.cleaned_data["flight"]
        )
        if flight_user.exists():
            flight_user = flight_user.first()
            flight_user.status = True
            flight_user.schedule_delay = form.cleaned_data["schedule_delay"]
            flight_user.save()
            return HttpResponseRedirect(reverse("tracking:list_tracking"))
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.status = True
        return super(TrackingCreateView, self).form_valid(form)


class TrackingListView(LoginRequiredMixin, ListView):
    """List of tracking tasks"""

    template_name = "tracking/list.html"
    model = models.FlightUser
    context_object_name = "user_flights"

    def get_queryset(self, *args, **kwargs):
        return models.FlightUser.objects.get_by_user(self.request.user)


class DisableTrackingView(LoginRequiredMixin, View):
    """Disable tracking task"""

    def get(self, request, *args, **kwargs):
        flight_user = get_object_or_404(models.FlightUser, pk=kwargs["pk"])
        flight_user.status = False
        flight_user.save()
        return HttpResponseRedirect(reverse("tracking:list_tracking"))


class EnableTrackingView(LoginRequiredMixin, View):
    """Disable tracking task"""

    def get(self, request, *args, **kwargs):
        flight_user = get_object_or_404(models.FlightUser, pk=kwargs["pk"])
        flight_user.status = True
        flight_user.save()
        return HttpResponseRedirect(reverse("tracking:list_tracking"))


class TrackingDeleteView(LoginRequiredMixin, DeleteView):
    """Delete tracking task"""

    model = models.FlightUser
    success_url = reverse_lazy("tracking:list_tracking")
