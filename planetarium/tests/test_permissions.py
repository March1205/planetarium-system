from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from planetarium.models import ShowTheme, AstronomyShow, PlanetariumDome, ShowSession, Reservation
from planetarium.serializers import ReservationListSerializer

SHOW_THEME_URL = reverse("planetarium:showtheme-list")
ASTRONOMY_SHOW_URL = reverse("planetarium:astronomyshow-list")
PLANETARIUM_DOME_URL = reverse("planetarium:planetariumdome-list")
SHOW_SESSION_URL = reverse("planetarium:showsession-list")
RESERVATION_URL = reverse("planetarium:reservation-list")


def sample_show_theme(name="Space Exploration"):
    return ShowTheme.objects.create(name=name)


def sample_astronomy_show(title="Black Holes", description="A show about black holes", theme=None, image=None):
    astronomy_show = AstronomyShow.objects.create(title=title, description=description, image=image)
    if theme:
        astronomy_show.theme.add(theme)
    return astronomy_show


def sample_planetarium_dome(name="Main Dome", rows=10, seats_in_row=10):
    return PlanetariumDome.objects.create(name=name, rows=rows, seats_in_row=seats_in_row)


def sample_show_session(show_time="2023-06-01T20:00:00Z", astronomy_show=None, planetarium_dome=None):
    if astronomy_show is None:
        astronomy_show = sample_astronomy_show()
    if planetarium_dome is None:
        planetarium_dome = sample_planetarium_dome()
    return ShowSession.objects.create(show_time=show_time, astronomy_show=astronomy_show, planetarium_dome=planetarium_dome)


def sample_reservation(user=None):
    if user is None:
        user = get_user_model().objects.create_user(email="user@example.com", password="testpass123")
    return Reservation.objects.create(user=user)


class ShowThemePermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="password123"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="adminpassword"
        )

    def test_create_show_theme_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        payload = {"name": "Galaxies"}
        response = self.client.post(SHOW_THEME_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_show_theme_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        payload = {"name": "Galaxies"}
        response = self.client.post(SHOW_THEME_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_show_themes_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(SHOW_THEME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_show_themes_as_unauthenticated_user(self):
        response = self.client.get(SHOW_THEME_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AstronomyShowPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="password123"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="adminpassword"
        )

    def test_create_astronomy_show_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            "title": "Supernova",
            "description": "Exploring supernovas"
        }
        response = self.client.post(ASTRONOMY_SHOW_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_astronomy_show_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "Supernova",
            "description": "Exploring supernovas"
        }
        response = self.client.post(ASTRONOMY_SHOW_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_astronomy_shows_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(ASTRONOMY_SHOW_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_astronomy_shows_as_unauthenticated_user(self):
        response = self.client.get(ASTRONOMY_SHOW_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PlanetariumDomePermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="password123"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="adminpassword"
        )

    def test_create_planetarium_dome_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        payload = {"name": "Dome A", "rows": 15, "seats_in_row": 15}
        response = self.client.post(PLANETARIUM_DOME_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_planetarium_dome_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        payload = {"name": "Dome A", "rows": 15, "seats_in_row": 15}
        response = self.client.post(PLANETARIUM_DOME_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_planetarium_domes_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(PLANETARIUM_DOME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_planetarium_domes_as_unauthenticated_user(self):
        response = self.client.get(PLANETARIUM_DOME_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ShowSessionPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="password123"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="adminpassword"
        )

    def test_create_show_session_as_admin(self):
        astronomy_show = sample_astronomy_show()
        planetarium_dome = sample_planetarium_dome()
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            "show_time": "2024-06-01T20:00:00Z",
            "astronomy_show": astronomy_show.id,
            "planetarium_dome": planetarium_dome.id
        }
        response = self.client.post(SHOW_SESSION_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_show_session_as_non_admin(self):
        astronomy_show = sample_astronomy_show()
        planetarium_dome = sample_planetarium_dome()
        self.client.force_authenticate(user=self.user)
        payload = {
            "show_time": "2024-06-01T20:00:00Z",
            "astronomy_show": astronomy_show.id,
            "planetarium_dome": planetarium_dome.id
        }
        response = self.client.post(SHOW_SESSION_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_show_sessions_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(SHOW_SESSION_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_show_sessions_as_unauthenticated_user(self):
        response = self.client.get(SHOW_SESSION_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReservationPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="password123"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="adminpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_reservation_as_authenticated_user(self):
        show_session = sample_show_session()
        payload = {
            "tickets": [
                {"row": 1, "seat": 1, "show_session": show_session.id},
                {"row": 1, "seat": 2, "show_session": show_session.id},
            ]
        }
        response = self.client.post(RESERVATION_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.get()
        self.assertEqual(reservation.tickets.count(), 2)

    def test_create_reservation_as_unauthenticated_user(self):
        self.client.force_authenticate(user=None)
        show_session = sample_show_session()
        payload = {
            "tickets": [
                {"row": 1, "seat": 1, "show_session": show_session.id},
                {"row": 1, "seat": 2, "show_session": show_session.id},
            ]
        }
        response = self.client.post(RESERVATION_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_reservations_as_authenticated_user(self):
        sample_reservation(user=self.user)
        sample_reservation(user=self.user)
        response = self.client.get(RESERVATION_URL)
        reservations = Reservation.objects.filter(user=self.user)
        serializer = ReservationListSerializer(reservations, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_list_reservations_as_unauthenticated_user(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(RESERVATION_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
