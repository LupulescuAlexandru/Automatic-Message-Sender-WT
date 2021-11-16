from django.urls import path
from .views import view_messages


urlpatterns = [
    path('view_messages/', view_messages, name="view-messages"),
]
