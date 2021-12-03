from django.urls import path, re_path
from .views import view_campaigns, create_campaign, send_msg, delete_campaign

urlpatterns = [
    path('view_campaigns/', view_campaigns, name="view-campaigns"),
    path('create_campaign/', create_campaign, name="create-campaign"),
    re_path(r'^send_msg/(?P<campaignid>\w+)/$', send_msg, name="send-msg"),
    re_path(r'^delete_campaign/(?P<campaignid>\w+)/$', delete_campaign, name="delete-campaigh"),
]
