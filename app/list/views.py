import csv
import re

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from person.models import Person

from .forms import CreateListForm, UpdateListForm
from .models import List


def check(input):
    email_regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    phone_regex = '^\+?1?\d{9,15}$'
    if re.search(email_regex, input):
        return 'Email'
    elif re.search(phone_regex, input):
        return 'Phone'
    return 0


@login_required
def create_list_view(request):
    form = CreateListForm(request.POST, request.FILES)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()

        if obj.csv_file:
            with open(obj.csv_file.path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        # validate email or phone number, skipping invalid fields
                        check_input = check(row[2])

                        if check_input == 'Email':
                            person, created = Person.objects.get_or_create(name=row[0], gender=row[1], email=row[2])
                        elif check_input == 'Phone':
                            person, created = Person.objects.get_or_create(name=row[0], gender=row[1], phone=row[2])

                        # we don't add the person to the list if it doesn't belong to the list type (ex: email in phone list)
                        # we accept both if the list is mixed
                        if obj.type != 'Mixt':
                            if check_input == obj.type:
                                obj.people.add(person)
                        else:
                            obj.people.add(person)

                        print(row[0])
                        line_count += 1

        return HttpResponseRedirect(reverse('view-list'))

    context = {
        'form': form
    }

    return render(request, "create_list.html", context)


@login_required
def view_lists(request):
    return render(request, "view_lists.html", {'lists': List.objects.all()})


@login_required
def update_list(request, listid):
    list_ = List.objects.get(id=listid)
    form = UpdateListForm(request.POST or None, instance=list_)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('view-list'))

    context = {
        'form': form
    }
    return render(request, "create_list.html", context)


@login_required
def delete_list(request, listid):
    List.objects.filter(id=listid).delete()
    return redirect(request.META['HTTP_REFERER'])
