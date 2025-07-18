from django.urls import path
from .views import Home, board_topics, new_topic
# app_name = "boards"

urlpatterns = [
    path("", Home, name="home"),
    path("<int:pk>/", board_topics, name="board_topics"),
    path("<int:pk>/new/", new_topic, name="new_topic"),
]
