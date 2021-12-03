from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Person
from .forms import CreateUpdatePersonForm


@login_required
def create_person(request):
    form = CreateUpdatePersonForm(request.POST or None)

    print(form.errors)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('view-people'))

    context = {
        'form': form
    }

    return render(request, "create_person.html", context)


@login_required
def view_people(request):
    return render(request, "view_people.html", {'people': Person.objects.all()})
