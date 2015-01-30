from django.http import HttpResponse
from django.conf import settings

class BasicAuthMiddleware(object):


    def process_request(self,request):
        authentication = request.META['HTTP_AUTHORIZATION']
        (authmeth, auth) = authentication.split(' ',1)
        if 'basic' != authmeth.lower():
            return self.unauthed()
        auth = auth.strip().decode('base64')
        username, password = auth.split(':',1)
