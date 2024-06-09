import os
import tempfile

from PIL import Image
from django.db.models import F, Count
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from planetarium.models import ShowTheme, AstronomyShow, PlanetariumDome, ShowSession, Reservation
from planetarium.serializers import (
    ShowThemeSerializer,
    AstronomyShowSerializer,
    PlanetariumDomeSerializer,
    ShowSessionListSerializer,
    ReservationListSerializer
)

SHOW_THEME_URL = reverse("planetarium:showtheme-list")
ASTRONOMY_SHOW_URL = reverse("planetarium:astronomyshow-list")
PLANETARIUM_DOME_URL = reverse("planetarium:planetariumdome-list")
SHOW_SESSION_URL = reverse("planetarium:showsession-list")
RESERVATION_URL = reverse("planetarium:reservation-list")


def sample_show_theme(name="Space Exploration"):
    return ShowTheme.objects.create(name=name)


def sample_astronomy_show(title="Black Holes", description="A show about black holes", theme=None, image=None):
    astronomy_show = AstronomyShow.objects.create(
        title=title, description=description, image=image
    )
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
    return ShowSession.objects.create(show_time=show_time, astronomy_show=astronomy_show,
                                      planetarium_dome=planetarium_dome)


def sample_reservation(user=None):
    if user is None:
        user = get_user_model().objects.create_user(email="user@example.com", password="testpass123")
    return Reservation.objects.create(user=user)


class ShowThemeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email="test@example.com", password="password123")
        self.user.is_staff = True  # Make the user an admin
        self.user.save()
        self.client.force_authenticate(self.user)

    def test_create_show_theme(self):
        payload = {"name": "Galaxies"}
        response = self.client.post(SHOW_THEME_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShowTheme.objects.count(), 1)
        self.assertEqual(ShowTheme.objects.get().name, payload["name"])

    def test_retrieve_show_themes(self):
        sample_show_theme(name="Stars")
        sample_show_theme(name="Planets")

        response = self.client.get(SHOW_THEME_URL)
        show_themes = ShowTheme.objects.all()
        serializer = ShowThemeSerializer(show_themes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class AstronomyShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email="test@example.com", password="password123")
        self.user.is_staff = True  # Make the user an admin
        self.user.save()
        self.client.force_authenticate(self.user)

    def test_create_astronomy_show(self):
        theme = sample_show_theme()
        payload = {
            "title": "Supernova",
            "description": "Exploring supernovas"
        }
        response = self.client.post(ASTRONOMY_SHOW_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AstronomyShow.objects.count(), 1)
        astronomy_show = AstronomyShow.objects.get()
        astronomy_show.theme.add(theme)  # Manually add the theme
        self.assertEqual(astronomy_show.title, payload["title"])
        self.assertEqual(astronomy_show.description, payload["description"])
        self.assertIn(theme, astronomy_show.theme.all())

    def test_retrieve_astronomy_shows(self):
        sample_astronomy_show(title="Nebulae")
        sample_astronomy_show(title="Exoplanets")

        response = self.client.get(ASTRONOMY_SHOW_URL)
        astronomy_shows = AstronomyShow.objects.all()
        serializer = AstronomyShowSerializer(astronomy_shows, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_upload_image_to_astronomy_show(self):
        astronomy_show = sample_astronomy_show()
        url = reverse('planetarium:astronomyshow-upload-image', args=[astronomy_show.id])
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            response = self.client.post(url, {"image": ntf}, format="multipart")
        astronomy_show.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("image", response.data)
        self.assertTrue(os.path.exists(astronomy_show.image.path))


class PlanetariumDomeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email="test@example.com", password="password123")
        self.user.is_staff = True  # Make the user an admin
        self.user.save()
        self.client.force_authenticate(self.user)

    def test_create_planetarium_dome(self):
        payload = {"name": "Dome A", "rows": 15, "seats_in_row": 15}
        response = self.client.post(PLANETARIUM_DOME_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PlanetariumDome.objects.count(), 1)
        planetarium_dome = PlanetariumDome.objects.get()
        self.assertEqual(planetarium_dome.name, payload["name"])
        self.assertEqual(planetarium_dome.rows, payload["rows"])
        self.assertEqual(planetarium_dome.seats_in_row, payload["seats_in_row"])

    def test_retrieve_planetarium_domes(self):
        sample_planetarium_dome(name="Dome B")
        sample_planetarium_dome(name="Dome C")

        response = self.client.get(PLANETARIUM_DOME_URL)
        planetarium_domes = PlanetariumDome.objects.all()
        serializer = PlanetariumDomeSerializer(planetarium_domes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class ShowSessionApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email="test@example.com", password="password123")
        self.user.is_staff = True  # Make the user an admin
        self.user.save()
        self.client.force_authenticate(self.user)

    def test_create_show_session(self):
        astronomy_show = sample_astronomy_show()
        planetarium_dome = sample_planetarium_dome()
        payload = {
            "show_time": "2024-06-01T20:00:00+0000",
            "astronomy_show": astronomy_show.id,
            "planetarium_dome": planetarium_dome.id
        }
        response = self.client.post(SHOW_SESSION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShowSession.objects.count(), 1)
        show_session = ShowSession.objects.get()
        self.assertEqual(show_session.show_time.strftime('%Y-%m-%dT%H:%M:%S%z'), payload["show_time"])

    def test_retrieve_show_sessions(self):
        sample_show_session()
        sample_show_session()

        response = self.client.get(SHOW_SESSION_URL)
        show_sessions = ShowSession.objects.all().annotate(
            tickets_available=(
                    F("planetarium_dome__rows") * F("planetarium_dome__seats_in_row")
                    - Count("tickets")
            )
        )
        serializer = ShowSessionListSerializer(show_sessions, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class ReservationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email="test@example.com", password="password123")
        self.client.force_authenticate(self.user)

    def test_create_reservation(self):
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

    def test_retrieve_reservations(self):
        sample_reservation(user=self.user)
        sample_reservation(user=self.user)

        response = self.client.get(RESERVATION_URL)
        reservations = Reservation.objects.filter(user=self.user)
        serializer = ReservationListSerializer(reservations, many=True)

        expected_response = {
            'count': reservations.count(),
            'next': None,
            'previous': None,
            'results': serializer.data
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)
