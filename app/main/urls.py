from django.urls import path
from .views import home, LoginPage, send_msg, logout_view

urlpatterns = [
    path('', home),
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('send_msg/', send_msg)
]

