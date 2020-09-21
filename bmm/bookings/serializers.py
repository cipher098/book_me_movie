from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
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

default_fields = ['id', 'uuid', 'created', 'modified', ]
default_readonly_fields = ['id', 'uuid', 'created', 'modified']


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        model_specific_fields = [
            'name',
            'description',
            'length',
            'cast',
            'director',
            'genre',
            'release_date',
            'certificate'
        ]
        fields = default_fields + model_specific_fields
        read_only_fields = default_readonly_fields


class TheatreSerializer(ModelSerializer):
    class Meta:
        model = Theatre
        model_specific_fields = [
            'name',
            'city'
        ]
        fields = default_fields + model_specific_fields
        read_only_fields = default_readonly_fields


class HallSerializer(ModelSerializer):
    class Meta:
        model = Hall
        model_specific_fields = [
            'name',
            'theatre'
        ]
        fields = default_fields + model_specific_fields
        read_only_fields = default_readonly_fields


class SeatTypeSerializer(ModelSerializer):
    class Meta:
        model = SeatType
        model_specific_fields = [
            'name',
            'price_multiplier',
            'theatre',
        ]
        fields = default_fields + model_specific_fields
        read_only_fields = default_readonly_fields


class SeatSerializer(ModelSerializer):
    class Meta:
        model = Seat
        model_specific_fields = [
            'row',
            'column',
            'seat_type',
            'hall',
        ]
        fields = default_fields + model_specific_fields
        read_only_fields = default_readonly_fields


class ShowSerializer(ModelSerializer):
    class Meta:
        model = Show
        model_specific_fields = [
            'start_time',
            'base_price',
            'movie',
            'hall',
        ]
        fields = default_fields + model_specific_fields
        read_only_fields = default_readonly_fields


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        model_specific_fields = [
            'price',
            'paid',
            'ticket_ids',
        ]
        fields = default_fields + model_specific_fields
        read_only_fields = default_readonly_fields


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        model_specific_fields = [
            'price',
            'show',
            'seat',
            'booking',
        ]
        fields = default_fields + model_specific_fields
        read_only_fields = default_readonly_fields
