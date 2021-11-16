from xml.dom import minidom

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import csv
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

from list.models import List
from .forms import LoginForm
from django.contrib import messages


@login_required
def home(request):
    return render(request, "index.html")


class LoginPage(LoginView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        loginForm = LoginForm()

        context = {
            'form': loginForm
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        loginForm = LoginForm(request.POST)  # create login form

        if loginForm.is_valid():
            password = loginForm.cleaned_data['password']  # get the password from the form
            username = loginForm.cleaned_data['username']  # get the username from the form

            # login user
            user = authenticate(request, username=username, password=password)

            confirmation = None

            if user is not None:
                login(request, user)
                confirmation = True

            if confirmation:
                return redirect("/")

            context = {
                'form': loginForm,
                'alert_flag': True
            }

            return render(request, self.template_name, context)


def logout_view(request):
    logout(request)
    return redirect('login')


def send_msg(request):
    with open(List.objects.get(id=2).csv_file.path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        field_obj = {}
        for field, field1 in zip(csv_reader[0], csv_reader[1]):
            field_obj[field] = field1

        print(field_obj)
        # for row in csv_reader:
        #     # column
        #     if line_count == 0:
        #
        #         line_count += 1
        #     else:
        #         print(row)
        #         line_count += 1

    return HttpResponseRedirect("/")
