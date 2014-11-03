__author__ = 'deathowl'
from urllib import quote
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.utils.datetime_safe import datetime
from django.utils import timezone
from schedule.models import Calendar
from schedule.utils import coerce_date_dict
from schedule.periods import weekday_names
from django.http import Http404
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.contrib import messages


@login_required()
def list(request):
    schedules = Calendar.objects.all()
    return TemplateResponse(request, 'schedule/list.html', {'schedules': schedules})

@login_required()
def delete(request, id):
    try:
        sched = Calendar.objects.get(id = id)
        sched.delete()
        return HttpResponseRedirect('/schedules/');
    except Calendar.DoesNotExist:
        raise Http404

@login_required()
def new(request):
    try:
        return TemplateResponse(request, 'schedule/edit.html', {})
    except Calendar.DoesNotExist:
        raise Http404

@login_required()
def details(request, id,  periods=None):
    try:
        sched = Calendar.objects.get(id = id)
        date = coerce_date_dict(request.GET)
        if date:
            try:
                date = datetime(**date)
            except ValueError:
                raise Http404
        else:
            date = timezone.now()
        event_list = sched.event_set.all()
        period_objects = dict([(period.__name__.lower(), period(event_list, date)) for period in periods])
        return render_to_response('schedule/detail.html',
         {
            'date': date,
            'periods': period_objects,
            'calendar': sched,
            'weekday_names': weekday_names,
            'here':quote(request.get_full_path()),
        },context_instance=RequestContext(request),
                                  )
    except Calendar.DoesNotExist:
        raise Http404

@login_required()
def edit(request, id):
    try:
        sched = Calendar.objects.get(id = id)
        return TemplateResponse(request, 'schedule/edit.html', {'item': sched})
    except Calendar.DoesNotExist:
        raise Http404
@login_required()
@require_http_methods(["POST"])
def save(request):
    try:
        sched = Calendar.objects.get(id = request.POST['id'])
    except Calendar.DoesNotExist:
        sched = Calendar()

    sched.name = request.POST['name']
    sched.slug = request.POST['slug']
    try:
        sched.save()
        return HttpResponseRedirect('/schedules/');
    except IntegrityError:
        messages.error(request, 'Schedule already exists')
        if int(request.POST['id']) > 0:
            return HttpResponseRedirect(reverse('openduty.schedules.edit', None, [str(request.POST['id'])]))
        else:
            return HttpResponseRedirect(reverse('openduty.schedules.new'))
