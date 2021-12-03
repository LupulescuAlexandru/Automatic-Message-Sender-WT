from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Message


@login_required
def view_messages(request):
    return render(request, "view_messages.html", {'messages': Message.objects.all()})
