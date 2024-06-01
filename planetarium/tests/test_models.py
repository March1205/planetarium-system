from django.test import TestCase

from user.models import User
from planetarium.models import PlanetariumDome, ShowTheme, AstronomyShow, ShowSession, Reservation, Ticket
from django.utils import timezone
from django.core.exceptions import ValidationError


class PlanetariumDomeTests(TestCase):

    def test_string_representation(self):
        dome = PlanetariumDome.objects.create(name="Alpha Dome", rows=10, seats_in_row=20)
        self.assertEqual(str(dome), "Alpha Dome")

    def test_capacity_calculation(self):
        dome = PlanetariumDome.objects.create(name="Alpha Dome", rows=10, seats_in_row=20)
        self.assertEqual(dome.capacity, 200)


class ShowThemeTests(TestCase):

    def test_string_representation(self):
        theme = ShowTheme.objects.create(name="Galaxy Exploration")
        self.assertEqual(str(theme), "Galaxy Exploration")


class AstronomyShowTests(TestCase):

    def test_string_representation(self):
        show = AstronomyShow.objects.create(title="Journey Through the Stars")
        self.assertEqual(str(show), "Journey Through the Stars")


class ShowSessionTests(TestCase):

    def test_string_representation(self):
        show = AstronomyShow.objects.create(title="Cosmic Voyage")
        dome = PlanetariumDome.objects.create(name="Beta Dome", rows=10, seats_in_row=15)
        session_time = timezone.now()
        session = ShowSession.objects.create(show_time=session_time, astronomy_show=show, planetarium_dome=dome)
        expected_str = f"{show.title} {session_time}"
        self.assertEqual(str(session), expected_str)


class ReservationTests(TestCase):

    def test_string_representation(self):
        user = User.objects.create_user(email='testuser@email.com', password='testpass123')
        reservation_time = timezone.now()
        reservation = Reservation.objects.create(user=user, created_at=reservation_time)
        self.assertEqual(str(reservation), str(reservation_time))


class TicketTests(TestCase):

    def test_string_representation_and_validation(self):
        user = User.objects.create_user(email='testuser@email.com', password='testpass123')
        reservation = Reservation.objects.create(user=user)
        show = AstronomyShow.objects.create(title="Stellar Journey")
        dome = PlanetariumDome.objects.create(name="Beta Dome", rows=5, seats_in_row=10)
        session = ShowSession.objects.create(show_time=timezone.now(), astronomy_show=show, planetarium_dome=dome)
        ticket = Ticket.objects.create(show_session=session, reservation=reservation, row=3, seat=7)
        expected_str = f"{str(session)} (row: 3, seat: 7)"
        self.assertEqual(str(ticket), expected_str)

    def test_ticket_validation(self):
        show = AstronomyShow.objects.create(title="Cosmic Journey")
        dome = PlanetariumDome.objects.create(name="Beta Dome", rows=5, seats_in_row=10)
        session = ShowSession.objects.create(show_time=timezone.now(), astronomy_show=show, planetarium_dome=dome)
        ticket = Ticket(show_session=session, row=6, seat=11)
        with self.assertRaises(ValidationError):
            ticket.clean()
