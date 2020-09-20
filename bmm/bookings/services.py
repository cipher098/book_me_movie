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


