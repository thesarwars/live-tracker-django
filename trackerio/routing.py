from django.urls import re_path

from .tracker_consumer import TrackerConsumer, CustomerTrackerConsumer

websocket_urlpatterns = [
    # Rider sends live location for an order
    re_path(
        r"api/v1/tracker/rider/(?P<order_id>\d+)/(?P<rider_id>\d+)/?$",
        TrackerConsumer.as_asgi(),
    ),
    # Customer subscribes to rider location for an order
    re_path(
        r"api/v1/tracker/customer/(?P<order_id>\d+)?$",
        CustomerTrackerConsumer.as_asgi(),
    ),
]