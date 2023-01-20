from django.conf.urls import url

from . import views

app_name = "tracking"
urlpatterns = [
    url(r"^create/$", views.TrackingCreateView.as_view(), name="create_tracking"),
    url(r"^list/$", views.TrackingListView.as_view(), name="list_tracking"),
    url(
        r"^disable/(?P<pk>\d+)/$",
        views.DisableTrackingView.as_view(),
        name="disable_tracking",
    ),
    url(
        r"^enable/(?P<pk>\d+)/$",
        views.EnableTrackingView.as_view(),
        name="enable_tracking",
    ),
    url(
        r"^delete/(?P<pk>\d+)/$",
        views.TrackingDeleteView.as_view(),
        name="delete_tracking",
    ),
]
