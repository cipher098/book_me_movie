import time
from celery.utils.log import get_task_logger
from celery import shared_task, chord, chain, group

from django.utils import timezone

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



import logging

logger = logging.getLogger(__name__)


class TicketServices:

    @staticmethod
    @shared_task(name="create_tickets_for_show", time_limit=60 * 30, soft_time_limit=60 * 30)
    def create_tickets_for_show(show_id):

        show = Show.objects.get(id=show_id)
        seats = show.hall.seats.all()

        tickets = []
        for seat in seats:
            ticket = Ticket(
                show=show,
                seat=seat,
                price=show.base_price * seat.seat_type.price_multiplier
            )
            tickets.append(ticket)

        Ticket.objects.bulk_create(tickets)

    @staticmethod
    def book_tickets(ticket_ids, booking_id):

        booking = Booking.objects.get(id=booking_id)

        tickets = []
        for ticket_id in ticket_ids:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.booking = booking
            tickets.append(ticket)

        Ticket.objects.bulk_update(tickets, ['booking'])


class BookingServices:

    @staticmethod
    @shared_task(name="delete_if_unpaid", time_limit=60 * 30, soft_time_limit=60 * 30)
    def delete_if_unpaid(booking_id=None):
        logger.info(f"Delete booking invoked for: {booking_id}")
        bookings = Booking.objects.filter(id=booking_id)

        for booking in bookings:
            booking_timedelta = (timezone.now() - booking.modified).seconds
            if not booking.paid and booking_timedelta >= 100:
                logger.info(f"Deleting Booking with ID: {booking.id} as it is unpaid"
                            f" and create more than {100} seconds ago.")
                booking.delete()
                booking.tickets.update(booking=None)

