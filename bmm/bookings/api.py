import logging
from io import BytesIO
from mimetypes import MimeTypes
from datetime import datetime
import django_filters

from celery.utils.log import get_task_logger
from celery import shared_task, chord, chain, group

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

import logging

logger = logging.getLogger(__name__)


from bmm.bookings.models import (
    Movie,
    Theatre,
    Hall,
    SeatType,
    Seat,
    Show,
    Booking,
    Ticket
)

from bmm.bookings.serializers import (
    MovieSerializer,
    TheatreSerializer,
    HallSerializer,
    SeatTypeSerializer,
    SeatSerializer,
    ShowSerializer,
    BookingSerializer,
    TicketSerializer,
)

from bmm.bookings.services import (
    TicketServices,
    BookingServices,
)

logger = logging.getLogger(__name__)

default_filterset_fields = ['id', 'uuid', 'created', 'modified']
default_ordering_fields = ['id', 'uuid', 'created', 'modified']
default_search_fields = ['id', 'uuid']


class MovieViewSet(viewsets.ModelViewSet):
    """
    MovieViewSet can be used to create/list/detail/update movies
    """
    lookup_field = "id"
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = default_filterset_fields + ['name', 'director', 'genre', 'release_date', 'certificate']
    search_fields = default_search_fields + ['name', 'director', 'genre', 'certificate']
    ordering_fields = default_ordering_fields + ['name', 'length', 'director', 'genre', 'release_date', 'certificate']
    ordering = ['-created']


class TheatreViewSet(viewsets.ModelViewSet):
    """
    TheatreViewSet can be used to create/list/detail/update theatre
    """
    lookup_field = "id"
    queryset = Theatre.objects.all()
    serializer_class = TheatreSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = default_filterset_fields + ['name', 'city']
    search_fields = default_search_fields + ['name', 'city']
    ordering_fields = default_ordering_fields + ['name', 'city']
    ordering = ['-created']


class HallViewSet(viewsets.ModelViewSet):
    """
    HallViewSet can be used to create/list/detail/update Hall
    """
    lookup_field = "id"
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = default_filterset_fields + ['name', 'theatre']
    search_fields = default_search_fields + ['name', 'theatre']
    ordering_fields = default_ordering_fields + ['name', 'theatre']
    ordering = ['-created']


class SeatTypeViewSet(viewsets.ModelViewSet):
    """
    SeatTypeViewSet can be used to create/list/detail/update SeatType
    """
    lookup_field = "id"
    queryset = SeatType.objects.all()
    serializer_class = SeatTypeSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = default_filterset_fields + ['name', 'price_multiplier', 'theatre']
    search_fields = default_search_fields + ['name', 'price_multiplier', 'theatre']
    ordering_fields = default_ordering_fields + ['name', 'price_multiplier', 'theatre']
    ordering = ['-created']


class SeatViewSet(viewsets.ModelViewSet):
    """
    SeatViewSet can be used to create/list/detail/update Seat
    """
    lookup_field = "id"
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = default_filterset_fields + ['row', 'column', 'seat_type', 'hall']
    search_fields = default_search_fields + ['row', 'column', 'seat_type', 'hall']
    ordering_fields = default_ordering_fields + ['row', 'column', 'seat_type', 'hall']
    ordering = ['-created']


class ShowViewSet(viewsets.ModelViewSet):
    """
    SeatViewSet can be used to create/list/detail/update Show
    """
    lookup_field = "id"
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = default_filterset_fields + ['start_time', 'base_price', 'movie', 'hall']
    search_fields = default_search_fields + ['start_time', 'base_price', 'movie', 'hall']
    ordering_fields = default_ordering_fields + ['start_time', 'base_price', 'movie', 'hall']
    ordering = ['-created']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        show_id = serializer.data.get('id', None)
        logger.info(f"Sending task for creating tickets for show id: {show_id}")
        TicketServices.create_tickets_for_show.apply_async((show_id,))
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BookingViewSet(viewsets.ModelViewSet):
    """
    BookingViewSet can be used to create/list/detail/update Booking
    """
    lookup_field = "id"
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = default_filterset_fields + ['price', 'paid']
    search_fields = default_search_fields + ['price', 'paid']
    ordering_fields = default_ordering_fields + ['price', 'paid']
    ordering = ['-created']


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tickets_data = TicketServices.check_availability(serializer.validated_data.get('ticket_ids', None))
        if tickets_data['available']:
            serializer.validated_data['price'] = tickets_data['booking_price']
            self.perform_create(serializer)
            TicketServices.book_tickets(
                serializer.data.get('ticket_ids', None),
                serializer.data.get('id', None)
            )
            BookingServices.delete_if_unpaid.apply_async((serializer.data.get('id', None),), countdown=100)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        else:
            response = {'error': f"Cannot complete booking because Tickets with ID's:"
                                 f" {tickets_data['already_booked_ticket_ids']} are"
                                 f" already booked. Please try booking other tickets."}
            return Response(response, status=status.HTTP_409_CONFLICT)




class TicketViewSet(viewsets.ModelViewSet):
    """
    TicketViewSet can be used to create/list/detail/update Ticket
    """
    lookup_field = "id"
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = default_filterset_fields + ['price', 'show', 'seat', 'booking']
    search_fields = default_search_fields + ['price', 'show', 'seat', 'booking']
    ordering_fields = default_ordering_fields + ['price', 'show', 'seat', 'booking']
    ordering = ['-created']
