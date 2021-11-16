from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import List


@login_required
def view_lists(request):
    return render(request, "view_lists.html", {'lists': List.objects.all()})
