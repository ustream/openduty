from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout;

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