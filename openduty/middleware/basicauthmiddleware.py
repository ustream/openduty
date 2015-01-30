from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout;
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

class BasicAuthMiddleware(object):

    def process_request(self,request):
        authentication = request.META.get('HTTP_AUTHORIZATION')
        if authentication:
            (authmeth, auth) = authentication.split(' ',1)
            if 'basic' == authmeth.lower():
                auth = auth.strip().decode('base64')
                username, password = auth.split(':',1)
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
