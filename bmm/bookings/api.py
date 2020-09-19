import logging
from io import BytesIO
from mimetypes import MimeTypes

import django_filters
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

from bmm.bookings.models import Movie
from bmm.bookings.serializers import MovieSerializer

logger = logging.getLogger(__name__)

default_filterset_fields = ['id', 'uuid', 'created', 'modified']
default_ordering_fields = ['id', 'uuid', 'created', 'modified']
default_search_fields = ['id', 'uuid']


class MovieViewSet(viewsets.ModelViewSet):
    """
    MovieViewSet can be used to create/list/detail/update actions
    """
    lookup_field = "id"
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = default_filterset_fields + ['name', 'director', 'genre', 'release_date', 'certificate']
    search_fields = default_search_fields + ['name', 'director', 'genre', 'certificate']
    ordering_fields = default_ordering_fields + ['name', 'length', 'director', 'genre', 'release_date', 'certificate']
    ordering = ['-created']

