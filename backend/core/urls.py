from django.urls import path
from .views import TestRunView

urlpatterns = [
    path("test/", TestRunView.as_view()),
]