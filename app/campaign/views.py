from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Campaign


@login_required
def view_campaigns(request):
    return render(request, "view_campaigns.html", {"campaigns": Campaign.objects.all()})
