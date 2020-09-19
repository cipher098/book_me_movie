from django.conf.urls import url
from rest_framework import routers

from bmm.bookings.api import MovieViewSet

app_name = "bookings"
api_router = routers.SimpleRouter(trailing_slash=False)
api_router.register(r'movies', MovieViewSet)

api_urlpatterns = api_router.urls

urlpatterns = api_urlpatterns
