import httplib
import urllib
from openduty.models import Incident

__author__ = 'gabo'

class ProwlNotifier:
    def __init__(self, config):
        self.__config = config

    def notify(self, notification):
        conn = httplib.HTTPSConnection("api.prowlapp.com", 443, timeout=10)
        try:
            description = notification.incident.description
            details = notification.incident.details
        except :
            description = notification.message
            details = ""
        conn.request("POST", "/publicapi/add",
          urllib.urlencode({
            "apikey": notification.user_to_notify.profile.prowl_api_key,
            "application" : notification.user_to_notify.profile.prowl_application or self.__config.get('application', 'openduty'),
            "url" : notification.user_to_notify.profile.prowl_url or "",
            "priority" : self.__config.get('priority', 0),
            "event" : description,
            "description": details,
          }), { "Content-type": "application/x-www-form-urlencoded" })
        status = conn.getresponse().status
        if 200 <= status < 300:
            print("Done")
        else:
            # todo: error handling
            print("Unable to connect.")