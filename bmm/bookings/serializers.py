from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
import logging

logger = logging.getLogger(__name__)

from bmm.bookings.models import Movie

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
