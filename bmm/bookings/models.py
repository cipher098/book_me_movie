from datetime import date

from django.db import models
from django.db.models import IntegerField
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields.json import JSONField
from django.contrib.postgres.fields import ArrayField

from bmm.utils.models import BaseModel


class Movie(BaseModel):
    """
       Movie Model represents movie.
    """

    name = models.CharField(
        verbose_name='Movie Name',
        null=False, blank=False,
        max_length=100,
    )

    description = models.TextField(verbose_name="Movie Description", null=True, blank=True)

    length = models.FloatField(
        verbose_name='Movie Lenght',
        null=False, blank=False,
    )

    cast = ArrayField(
        models.CharField(max_length=100, blank=False)
    )

    director = models.CharField(
        verbose_name='Movie Director',
        null=False, blank=False,
        max_length=100,
    )

    GENRE_THRILLER = 'THRILLER'
    GENRE_DRAMA = 'DRAMA'
    GENRE_HORROR = 'HORROR'
    GENRE_ACTION = 'ACTION'
    GENRE_COMEDY = 'COMEDY'
    GENRE_ADVENTURE = 'ADVENTURE'
    GENRE_SCI_FI = 'SCI_FI'
    GENRE_ROMANCE = 'ROMANCE'
    GENRE_ANIMATION = 'ANIMATION'
    GENRE_FANTASY = 'FANTASY'
    GENRE_CRIME = 'CRIME'
    GENRE_MYSTERY = 'MYSTERY'
    GENRE_SUPERHERO = 'SUPERHERO'
    GENRE_CHOICES = [
        (GENRE_THRILLER, _('Thriller')),
        (GENRE_DRAMA, _('Drama')),
        (GENRE_HORROR, _('Horror')),
        (GENRE_ACTION, _('Action')),
        (GENRE_COMEDY, _('Comedy')),
        (GENRE_ADVENTURE, _('Adventure')),
        (GENRE_SCI_FI, _('Sci-Fi')),
        (GENRE_ROMANCE, _('Romance')),
        (GENRE_ANIMATION, _('Animation')),
        (GENRE_FANTASY, _('Fantasy')),
        (GENRE_CRIME, _('Crime')),
        (GENRE_MYSTERY, _('Mystery')),
        (GENRE_SUPERHERO, _('Superhero')),
    ]

    genre = models.CharField(
        verbose_name='Genre of Movie',
        null=True, blank=True, default="",
        choices=GENRE_CHOICES,
        max_length=100,
    )

    release_date = models.DateField(
        verbose_name='Movie Release Date',
        null=False, blank=False, default=date.today()
    )

    CERTIFICATE_A = 'A'
    CERTIFICATE_UA = 'UA'
    CERTIFICATE_U = 'U'
    CERTIFICATE_S = 'S'
    CERTIFICATE_CHOICES = [
        (CERTIFICATE_A, _('A')),
        (CERTIFICATE_UA, _('U/A')),
        (CERTIFICATE_U, _('U')),
        (CERTIFICATE_S, _('S')),
    ]

    certificate = models.CharField(
        verbose_name='Certificate of Movie',
        null=False, blank=False,
        choices=CERTIFICATE_CHOICES,
        max_length=100,
    )

    # class Meta:
    #     db_table = 'movie'
    #     app_label = 'bookings.movie'

    def __str__(self):
        return f"Movie[id={self.id} uuid={self.uuid} name={self.name}]"


class Theatre(BaseModel):
    """
       Theatre Model represents theatre.
    """

    name = models.CharField(
        verbose_name='Theatre Name',
        null=False, blank=False,
        max_length=100,
    )

    city = models.CharField(
        verbose_name='Theatre City',
        null=False, blank=False,
        max_length=100,
    )

    # default_show_price_before_12 = models.IntegerField(
    #     verbose_name='Default Show price Before 12PM',
    #     null=False, blank=False,
    # )
    #
    # default_show_price_after_12 = models.IntegerField(
    #     verbose_name='Default Show price After 12PM',
    #     null=False, blank=False,
    # )


    # class Meta:
    #     db_table = 'smart_parser_parser'

    def __str__(self):
        return f"Theatre[id={self.id} uuid={self.uuid} name={self.name}]"


class Hall(BaseModel):
    """
       Hall Model represents hall in theatre.
    """

    name = models.CharField(
        verbose_name='Hall Name',
        null=False, blank=False,
        max_length=100,
    )

    theatre = models.ForeignKey(
        Theatre,
        verbose_name='Theatre',
        related_name='halls',
        null=False, blank=False, on_delete=models.CASCADE,
    )

    # class Meta:
    #     db_table = 'smart_parser_parser'

    def __str__(self):
        return f"Hall[id={self.id} uuid={self.uuid} name={self.name}]"


class SeatType(BaseModel):
    """
       SeatType Model represents SeatType in theatre.
    """

    name = models.CharField(
        verbose_name='Seat Type Name',
        null=False, blank=False,
        max_length=100,
    )

    price_multiplier = models.FloatField(
        verbose_name='Price Multiplier',
        null=False, blank=False,
    )

    theatre = models.ForeignKey(
        Theatre,
        verbose_name='Theatre',
        related_name='seat_types',
        null=False, blank=False, on_delete=models.CASCADE,
    )

    # class Meta:
    #     db_table = 'smart_parser_parser'

    def __str__(self):
        return f"Seat Type[id={self.id} uuid={self.uuid} name={self.name}]"


class Seat(BaseModel):
    """
       Seat Model represents Seat in Hall.
    """

    row = models.CharField(
        verbose_name='Seat Row',
        null=False, blank=False,
        max_length=100,
    )

    column = models.CharField(
        verbose_name='Seat Column',
        null=False, blank=False,
        max_length=100,
    )

    seat_type = models.ForeignKey(
        SeatType,
        verbose_name='Seat Type',
        related_name='seats',
        null=False, blank=False, on_delete=models.CASCADE,
    )

    hall = models.ForeignKey(
        Hall,
        verbose_name='Hall',
        related_name='seats',
        null=False, blank=False, on_delete=models.CASCADE,
    )

    # class Meta:
    #     db_table = 'smart_parser_parser'

    def __str__(self):
        return f"Seat [id={self.id} uuid={self.uuid} name={self.name}]"


class Show(BaseModel):
    """
       Show Model represents Show playing in theatre.
    """

    start_time = models.DateTimeField(
        verbose_name='Start Time',
        null=False, blank=False
    )

    end_time = models.DateTimeField(
        verbose_name='End Time',
        null=False, blank=False
    )

    base_price = models.FloatField(
        verbose_name='Price Multiplier',
        null=False, blank=False,
    )

    movie = models.ForeignKey(
        Movie,
        verbose_name='Movie',
        related_name='shows',
        null=False, blank=False, on_delete=models.CASCADE,
    )

    hall = models.ForeignKey(
        Hall,
        verbose_name='Hall',
        related_name='shows',
        null=False, blank=False, on_delete=models.CASCADE,
    )

    # class Meta:
    #     db_table = 'smart_parser_parser'

    def __str__(self):
        return f"Show [id={self.id} uuid={self.uuid} name={self.name}]"


class Booking(BaseModel):
    """
       Ticket Model represents Ticket Booked by user.
    """

    price = models.FloatField(
        verbose_name='Price',
        null=False, blank=False,
    )

    tax = models.FloatField(
        verbose_name='Tax',
        null=False, blank=False,
    )

    paid = models.BooleanField(
        verbose_name='Is payment recieved for Booking?',
        null=False, blank=False, default=False
    )

    # class Meta:
    #     db_table = 'smart_parser_parser'

    def __str__(self):
        return f"Booking [id={self.id} uuid={self.uuid} name={self.name}]"



class Ticket(BaseModel):
    """
       Ticket Model represents Ticket Booked by user.
    """

    price = models.FloatField(
        verbose_name='Price',
        null=False, blank=False,
    )

    show = models.ForeignKey(
        Show,
        verbose_name='Show',
        related_name='tickets',
        null=False, blank=False, on_delete=models.CASCADE,
    )

    seat = models.ForeignKey(
        Seat,
        verbose_name='Seat',
        related_name='tickets',
        null=False, blank=False, on_delete=models.CASCADE,
    )

    booking = models.ForeignKey(
        Booking,
        verbose_name='Booking',
        related_name='tickets',
        null=True, blank=True, default=None, on_delete=models.SET_NULL,
    )

    # class Meta:
    #     db_table = 'smart_parser_parser'

    def __str__(self):
        return f"Show [id={self.id} uuid={self.uuid} name={self.name}]"
