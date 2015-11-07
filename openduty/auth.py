from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout;
from rest_framework.permissions import BasePermission, SAFE_METHODS


def login(request):
    redirect_to = request.GET.get("next", "/dashboard/")
    return TemplateResponse(request, 'auth/login.html', {"redirect_to": redirect_to})

def do(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    redirect_to = request.POST['redirect_to']
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect(redirect_to)
    else:
        return HttpResponseRedirect('/login/')

def logout(request):
    auth_logout(request);
    return HttpResponseRedirect('/login/')



class IsAuthenticatedOrCreateOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return (
            request.method not in SAFE_METHODS or
            request.user and
            request.user.is_authenticated()
        )
