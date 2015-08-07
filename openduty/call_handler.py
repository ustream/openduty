from django.http import HttpResponse

__author__ = 'deathowl'
from twilio import twiml
from django.contrib.auth.models import User
from openduty.models import Incident
from notification.models import ScheduledNotification
from openduty.incidents import _update_type
from django_twilio.decorators import twilio_view

@twilio_view
def read_notification(request, id, user_id):
    resp = twiml.Response()
    try:
        notification = ScheduledNotification.objects.get(id=id)
        user = User.objects.get(id=user_id)
        resp.say("Hello %s" % user.username)
        resp.say(notification.message)
        with resp.gather(numDigits=1, action="/twilio/handle/%s/%s" % (id, user_id), method="GET") as g:
            g.say("Press 1 to Acknowledge")
            g.say("Press 2 to Resolve")
            g.say("Press 3 to do nothing")
    except ScheduledNotification.DoesNotExist:
        resp.say("Incident already resolved. Lucky you.")
    except User.DoesNotExist:
        resp.say("Go away, scriptkiddie.")
    return resp

@twilio_view
def handle_key(request, id, user_id):
    """Handle key press from a user."""
    digit_pressed = request.GET.get('Digits', None)
    resp = twiml.Response()
    try:
        notification = ScheduledNotification.objects.get(id=id)
        user = User.objects.get(id=user_id)
        if digit_pressed == "1":
            resp.say("Incident Acknowledged")
            _update_type(user, [notification.incident.id], Incident.ACKNOWLEDGE)
        if digit_pressed == "2":
            resp.say("Incident Resolved")
            _update_type(user, [notification.incident.id], Incident.RESOLVE)
        if digit_pressed == "3":
            notification.delete()
            resp.say("You are a terrible person.")
    except ScheduledNotification.DoesNotExist:
        resp.say("Incident already resolved. Lucky you.")
    except User.DoesNotExist:
        resp.say("Go away, scriptkiddie.")
    return resp
