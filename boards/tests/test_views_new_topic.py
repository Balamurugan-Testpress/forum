from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from boards.views import new_topic
from boards.models import Board, Topic, Post
from boards.forms import NewTopicForm


class NewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="django", description="django board")
        self.user = User.objects.create_user(
            username="john", email="john@doe.com", password="123"
        )
        self.client.login(username="john", password="123")
        self.url = reverse("new_topic", kwargs={"pk": self.board.pk})

    def test_new_topic_view_status_code_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_new_topic_view_status_code_not_found(self):
        url = reverse("new_topic", kwargs={"pk": 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_new_topic_url_resolves_correct_view(self):
        url = f"/board/{self.board.pk}/new/"
        view = resolve(url)
        self.assertEqual(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board(self):
        board_topics_url = reverse("board_topics", kwargs={"pk": self.board.pk})
        response = self.client.get(self.url)
        self.assertContains(response, f'href="{board_topics_url}"')

    def test_new_topic_view_contains_csrf_token(self):
        response = self.client.get(self.url)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_new_topic_form_submission_valid_data(self):
        data = {"subject": "Test title", "message": "Lorem ipsum dolor sit amet"}
        response = self.client.post(self.url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_form_submission_empty_fields(self):
        data = {"subject": "", "message": ""}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_new_topic_view_contains_form_instance(self):
        response = self.client.get(self.url)
        form = response.context.get("form")
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_form_submission_invalid_data(self):
        response = self.client.post(self.url, {})
        form = response.context.get("form")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)


class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name="Django", description="Django board.")
        self.url = reverse("new_topic", kwargs={"pk": 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse("login")
        self.assertRedirects(
            self.response,
            "{login_url}?next={url}".format(login_url=login_url, url=self.url),
        )
