from django.urls import path
from . import views

app_name = "sms"

urlpatterns = [
    path("", views.send_view, name="send"),
    path("history/", views.history_view, name="history"),
]
