import datetime
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from schedule.forms import EventForm
from schedule.models import Calendar, Event
from schedule.utils import coerce_date_dict, check_event_permissions
from schedule.views import get_next_url
from .models import User


__author__ = 'deathowl'

@check_event_permissions
def create_or_edit_event(request, calendar_slug, event_id=None, next=None,
    template_name='event/edit.html', form_class = EventForm):
    date = coerce_date_dict(request.GET)
    initial_data = None
    if date:
        try:
            start = datetime.datetime(**date)
            initial_data = {
                "start": start,
                "end": start + datetime.timedelta(minutes=30)
            }
        except TypeError:
            raise Http404
        except ValueError:
            raise Http404

    instance = None
    if event_id is not None:
        instance = get_object_or_404(Event, id=event_id)

    calendar = get_object_or_404(Calendar, slug=calendar_slug)
    data = request.POST.copy()
    if data:
        data["title"] = data["oncall"]+","+data["fallback"]
    form = form_class(data=data or None, instance=instance, initial=initial_data)
    users = User.objects.all();
    if form.is_valid():
        event = form.save(commit=False)
        if instance is None:
            event.creator = request.user
            event.calendar = calendar
        event.save()
        return HttpResponseRedirect(reverse('calendar_details', kwargs={'calendar_slug': calendar.slug}))
    if instance is not None:
        officers = instance.title.split(",")
        data["oncall"] = officers[0]
        data["fallback"] = officers[1]
        data["start_ymd"] = instance.start.date().isoformat()
        data["start_hour"] = instance.start.time().strftime("%H:%M")
        data["end_ymd"] = instance.end.date().isoformat()
        data["end_hour"] = instance.end.time().strftime("%H:%M")
        if instance.end_recurring_period:
            data["recurr_ymd"] = instance.end_recurring_period.date().isoformat()
        data["description"] = instance.description
        data["rule"] = instance.rule and instance.rule.id or ""


    next = get_next_url(request, next)
    return render_to_response(template_name, {
        "data": data,
        "calendar": calendar,
        "next":next,
        "users":users,
        "form": form,
    }, context_instance=RequestContext(request))

@check_event_permissions
def destroy_event(request, calendar_slug, event_id=None, next=None,
    template_name='', form_class = EventForm):
    instance = None
    if event_id is not None:
        instance = get_object_or_404(Event, id=event_id)

    if instance is not None:
        instance.delete()

    calendar = get_object_or_404(Calendar, slug=calendar_slug)

    return HttpResponseRedirect(reverse('calendar_details', None, [str(calendar.slug)]))
