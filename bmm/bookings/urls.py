from django.conf.urls import url
from rest_framework import routers

from bmm.bookings.api import MovieViewSet
from bmm.bookings.api import (
    MovieViewSet,
    TheatreViewSet,
    HallViewSet,
    SeatTypeViewSet,
    SeatViewSet,
    ShowViewSet,
    BookingViewSet,
    TicketViewSet,
)


app_name = "bookings"
api_router = routers.SimpleRouter(trailing_slash=False)
api_router.register(r'movies', MovieViewSet)
api_router.register(r'theatres', TheatreViewSet)
api_router.register(r'halls', HallViewSet)
api_router.register(r'seat_types', SeatTypeViewSet)
api_router.register(r'seats', SeatViewSet)
api_router.register(r'shows', ShowViewSet)
api_router.register(r'bookings', BookingViewSet)
api_router.register(r'tickets', TicketViewSet)

api_urlpatterns = api_router.urls

urlpatterns = api_urlpatterns
