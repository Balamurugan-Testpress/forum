from django import urls
from django.http import response
from django.test import TestCase
from django.urls import reverse
from .models import Board


class HomeViewTests(TestCase):
    def setUp(self) -> None:
        Board.objects.create(name="Sample Board", description="Sample Description")

    def test_status_code(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_template(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "boards/home.html")

    def test_home_view_context_contains_boards(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertIn("boards", response.context)
        self.assertEqual(len(response.context["boards"]), 1)
        self.assertEqual(response.context["boards"][0].name, "Sample Board")
