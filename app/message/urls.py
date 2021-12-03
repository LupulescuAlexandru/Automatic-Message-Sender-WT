from django.urls import path, re_path
from .views import create_message, view_messages, choose_fields, view_message, delete_message, choose_type, \
    create_html_message

urlpatterns = [
    path('choose_type/', choose_type, name="choose-type"),
    path('create_message/', create_message, name="create-message"),
    path('create_html_message/', create_html_message, name="create-html-message"),
    re_path(r'^choose_fields/(?P<messageid>\w+)/$', choose_fields, name="choose-fields"),
    re_path(r'^view_message/(?P<messageid>\w+)/$', view_message, name="view-message"),
    re_path(r'^delete_message/(?P<messageid>\w+)/$', delete_message, name="delete-message"),
    path('view_messages/', view_messages, name="view-messages"),
]
