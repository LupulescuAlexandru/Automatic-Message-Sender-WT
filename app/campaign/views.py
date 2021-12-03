import os
from email.mime.image import MIMEImage
import re

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Campaign

from django.core.mail import EmailMultiAlternatives
from app.settings import EMAIL_HOST_USER

from .forms import CreateCampaignForm

API_KEY = os.environ.get("SMSO_API_KEY")


@login_required
def create_campaign(request):
    form = CreateCampaignForm(request.POST, request.FILES)
    errors = None

    if form.is_valid():
        if form.cleaned_data['list'].type != 'Email' and form.cleaned_data['message'].html:
            errors = 'Can\'t bind mixed or phone list with HTML message'
        else:
            form.save()
            return HttpResponseRedirect(reverse('view-campaigns'))

    context = {
        'form': form,
        'errors': errors
    }

    return render(request, "create_campaign.html", context)


@login_required
def view_campaigns(request):
    return render(request, "view_campaigns.html", {"campaigns": Campaign.objects.all()})


@login_required
def delete_campaign(request, campaignid):
    Campaign.objects.filter(id=campaignid).delete()
    return redirect(request.META['HTTP_REFERER'])


def check(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if re.search(regex, email):
        return 1
    return 0


@login_required()
def send_msg(request, campaignid):
    try:
        campaign_obj = Campaign.objects.get(id=campaignid)
        print(API_KEY)
        sms_ids = requests.get("https://app.smso.ro/api/v1/senders/?apiKey=" + API_KEY)
        print(sms_ids)
        if sms_ids.status_code == 200:
            sms_ids = sms_ids.json()[0]['id']
        else:
            raise Http404

        people_queryset = campaign_obj.list.people.all()

        for person in people_queryset:
            if campaign_obj.message.diff_gender and person.gender == 'F':
                message = campaign_obj.message.message_female.replace('{name}', person.name)
            else:
                message = campaign_obj.message.message.replace('{name}', person.name)

            if person.email:
                images = re.findall(r'src="cid:(.*?)"', message)
                email_content = EmailMultiAlternatives(
                    campaign_obj.title,
                    message,
                    EMAIL_HOST_USER,
                    [person.email]
                )
                email_content.attach_alternative(message, "text/html")
                email_content.mixed_subtype = 'related'

                media_path = 'media/uploads/images/'

                for f in images:
                    fp = open(os.path.join(media_path, f), 'rb')
                    img = MIMEImage(fp.read())
                    fp.close()
                    img.add_header('Content-ID', '<{}>'.format(f))
                    email_content.attach(img)

                email_content.send()
            elif person.phone:
                url = 'https://app.smso.ro/api/v1/send/?apiKey=' + API_KEY
                payload = {'to': person.phone,
                           'sender': sms_ids,
                           'body': message}
                requests.post(url, data=payload)

    except Exception as e:
        print(e)
        raise Http404

    return HttpResponseRedirect(reverse('view-campaigns'))
