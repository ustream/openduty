__author__ = "dzsubek"

from notification.models import UserNotificationMethod
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from .models import User, UserProfile
from django.http import Http404
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.contrib import messages

@login_required()
def list(request):
    users = User.objects.all();
    return TemplateResponse(request, 'users/list.html', {'users': users})

@login_required()
def delete(request, id):
    try:
        user = User.objects.get(id = id)
        user.delete()
        return HttpResponseRedirect('/users/');
    except User.DoesNotExist:
        raise Http404

@login_required()
def edit(request, id):
    try:
        user = User.objects.get(id = id)
        user_methods = UserNotificationMethod.objects.filter(user = user).order_by('position')

        return TemplateResponse(
            request, 'users/edit.html',
            {'item': user, 'methods': UserNotificationMethod.methods, 'user_methods': user_methods, 'empty_user_method': UserNotificationMethod()}
        )
    except User.DoesNotExist:
        raise Http404

@login_required()
def new(request):
    return TemplateResponse(request, 'users/edit.html', {'methods': UserNotificationMethod.methods, 'empty_user_method': UserNotificationMethod()})

@login_required()
@require_http_methods(["POST"])
def save(request):
    try:
        user = User.objects.get(id = request.POST['id'])
    except User.DoesNotExist:
        user = User()
        user.is_active = True

    user.username = request.POST['username']
    user.email = request.POST['email']
    if request.POST['password']:
        user.set_password(request.POST['password'])

    try:
        user.save()
        try:
            UserNotificationMethod.objects.filter(user=user).delete()
        except UserNotificationMethod.DoesNotExist:
            pass #Nothing to clear
        methods = request.POST.getlist('methods[]')
        for idx, item in enumerate(methods):
            method = UserNotificationMethod()
            method.method = item
            method.user = user
            method.position = idx +1
            method.save()
        try:
            profile = user.get_profile()
        except UserProfile.DoesNotExist:
            profile = UserProfile()
            profile.user = user
        profile.phone_number = request.POST['phone_number']
        profile.pushover_user_key = request.POST['pushover_user_key']
        profile.pushover_app_key = request.POST['pushover_app_key']
        profile.slack_room_name = request.POST['slack_room_name']
        profile.save()

        return HttpResponseRedirect('/');
    except IntegrityError:
        messages.error(request, 'Username already exists.')
        if int(request.POST['id']) > 0:
            return HttpResponseRedirect(reverse('openduty.users.edit', None, [str(request.POST['id'])]))
        else:
            return HttpResponseRedirect(reverse('openduty.users.new'))