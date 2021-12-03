import csv
import re

from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Message

from .forms import CreateMessageForm, ChooseFields


@login_required()
def choose_type(request):
    return render(request, "choose_type.html", {})


@login_required
def create_message(request):
    form = CreateMessageForm(request.POST, request.FILES)
    if form.is_valid():
        initial_obj = form.save(commit=False)
        initial_obj.save()
        path = initial_obj.csv_fields.path
        field_dict = {}
        to_fill_fields = re.findall(r'{xx[0-9]+}', initial_obj.message)

        if initial_obj.diff_gender:
            for key in re.findall(r'{xx[0-9]+}', initial_obj.message_female):
                to_fill_fields.append(key)

        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            keys = next(csv_reader)
            values = next(csv_reader)
            for key, value in zip(keys, values):
                field_dict[key] = value

        CHOICES = []
        for key in keys:
            CHOICES.append((key, key))

        id = str(initial_obj.id)
        request.session['FILL_FIELDS' + id] = to_fill_fields
        request.session['CHOICES' + id] = CHOICES
        request.session['FIELD_DICT' + id] = field_dict

        return HttpResponseRedirect(reverse('choose-fields', kwargs={'messageid': initial_obj.id}))

    context = {
        'form': form
    }

    return render(request, "create_message.html", context)


@login_required
def create_html_message(request):
    form = CreateMessageForm(request.POST, request.FILES)
    if 'submit_form' in request.POST:
        if form.is_valid():
            initial_obj = form.save(commit=False)
            initial_obj.html = True
            initial_obj.save()
            path = initial_obj.csv_fields.path
            field_dict = {}
            to_fill_fields = re.findall(r'{xx[0-9]+}', initial_obj.message)

            if initial_obj.diff_gender:
                for key in re.findall(r'{xx[0-9]+}', initial_obj.message_female):
                    to_fill_fields.append(key)
            with open(path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                keys = next(csv_reader)
                values = next(csv_reader)
                for key, value in zip(keys, values):
                    field_dict[key] = value

            CHOICES = []
            for key in keys:
                CHOICES.append((key, key))

            id = str(initial_obj.id)
            request.session['FILL_FIELDS' + id] = to_fill_fields
            request.session['CHOICES' + id] = CHOICES
            request.session['FIELD_DICT' + id] = field_dict

            return HttpResponseRedirect(reverse('choose-fields', kwargs={'messageid': initial_obj.id}))

    elif 'preview_form' in request.POST:
        if form.is_valid():
            initial_obj = form.save(commit=False)
            content = initial_obj.message
            formatted_content = content.replace('cid:', '/media/uploads/images/')
            context = {
                'message': formatted_content
            }

            return render(request, "preview_html.html", context)

    context = {
        'form': form,
    }

    return render(request, "create_html_message.html", context)


@login_required
def choose_fields(request, messageid):
    if messageid:
        new_fields = {}
        FILL_FIELDS = request.session.get("FILL_FIELDS" + messageid)
        CHOICES = request.session.get("CHOICES" + messageid)
        FIELD_DICT = request.session.get("FIELD_DICT" + messageid)

        for field in FILL_FIELDS:
            new_fields[field] = forms.CharField(widget=forms.Select(choices=CHOICES))

        DynamicFieldForm = type('DynamicIngridientsForm',
                                (ChooseFields,),
                                new_fields)
        form = DynamicFieldForm(request.POST or None)

        if form.is_valid():
            try:
                message_obj = Message.objects.get(id=messageid)

                step = 1
                if message_obj.diff_gender:
                    step = 2

                for i in range(step):
                    print(i)
                    new_msg = message_obj.message if i == 0 else message_obj.message_female
                    for field in FILL_FIELDS:
                        new_msg = new_msg.replace(field, FIELD_DICT[form.cleaned_data[field]])
                    if i == 0:
                        message_obj.message = new_msg
                    else:
                        message_obj.message_female = new_msg
                    message_obj.save()

                request.session.modified = True
                del request.session["FILL_FIELDS" + messageid]
                del request.session["CHOICES" + messageid]
                del request.session["FIELD_DICT" + messageid]
                return HttpResponseRedirect(reverse('view-message', kwargs={'messageid': message_obj.id}))

            except Message.DoesNotExist:
                return render(request, "choose_fields.html", {'form': form})

        return render(request, "choose_fields.html", {'form': form})


@login_required
def view_messages(request):
    return render(request, "view_messages.html", {'messages': Message.objects.all()})


@login_required
def delete_message(request, messageid):
    Message.objects.filter(id=messageid).delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required
def view_message(request, messageid):
    print(Message.objects.get(id=int(messageid)))
    return render(request, "view_message.html", {'message': Message.objects.get(id=messageid)})
