from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from boards.models import Board


class HomeViewTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(
            name="Sample Board", description="Sample Description"
        )
        self.url = reverse("home")
        self.response = self.client.get(self.url)

    def test_home_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_home_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "boards/home.html")

    def test_home_context_contains_boards(self):
        boards = self.response.context["boards"]
        self.assertIn("boards", self.response.context)
        self.assertEqual(len(boards), 1)
        self.assertEqual(boards[0].name, "Sample Board")

    def test_home_contains_link_to_board_topics(self):
        board_topics_url = reverse("board_topics", kwargs={"pk": self.board.pk})
        self.assertContains(self.response, f'href="{board_topics_url}"')
