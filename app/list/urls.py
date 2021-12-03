from django.urls import path, re_path
from .views import create_list_view, view_lists, delete_list, update_list

urlpatterns = [
    path('create_list/', create_list_view),
    path('view_lists/', view_lists, name="view-list"),
    re_path(r'^delete_list/(?P<listid>\w+)/$', delete_list, name="delete-list"),
    re_path(r'^update_list/(?P<listid>\w+)/$', update_list, name="update-list"),
]
