from django.shortcuts import render

from django import forms
from .models import Image
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CreateImageForm


@login_required
def add_image_view(request):
    form = CreateImageForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('view-images'))

    context = {
        'form': form
    }

    return render(request, "add_image.html", context)


@login_required()
def view_images(request):

    context = {
        'images': Image.objects.all()
    }

    return render(request, "view_images.html", context)


@login_required
def delete_image(request, imageid):
    Image.objects.filter(id=imageid).delete()
    return redirect(request.META['HTTP_REFERER'])


