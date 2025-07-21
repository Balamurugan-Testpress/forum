from django.test import TestCase
from django.urls import resolve, reverse

from boards.views import TopicListView, board_topics
from boards.models import Board


class BoardTopicsTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="django", description="django board")

    def test_board_topics_view_status_code_success(self):
        url = reverse("board_topics", kwargs={"pk": self.board.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_board_topics_view_status_code_not_found(self):
        url = reverse("board_topics", kwargs={"pk": 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_board_topics_url_resolves_correct_view(self):
        url = f"/board/{self.board.pk}/"
        view = resolve(url)
        self.assertEqual(view.func, board_topics)

    def test_board_topics_view_contains_home_link(self):
        url = reverse("board_topics", kwargs={"pk": self.board.pk})
        response = self.client.get(url)
        home_url = reverse("home")
        self.assertContains(response, f'href="{home_url}"')

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse("board_topics", kwargs={"pk": self.board.pk})
        new_topic_url = reverse("new_topic", kwargs={"pk": self.board.pk})
        home_url = reverse("home")
        response = self.client.get(board_topics_url)
        self.assertContains(response, f'href="{home_url}"')
        self.assertContains(response, f'href="{new_topic_url}"')

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve("/board/1/")
        self.assertEqual(view.func.view_class, TopicListView)
