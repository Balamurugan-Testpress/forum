from django.urls import path
from .views import Home
# app_name = "boards"

urlpatterns = [path("", Home, name="home")]
