from .models import Image
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def view_images(request):
    context = {
        'images': Image.objects.all()
    }

    return render(request, "view_images.html", context)
