__author__ = 'deathowl'

from twilio.rest import TwilioRestClient
import twilio
import sys

class TwilioSmsNotifier:

    def __init__(self, config):
        self.__config = config

    def notify(self, notification):
        max_length = 160
        message = (notification.message[:max_length-2] + '..') if len(notification.message) > max_length else notification.message
        client = TwilioRestClient(self.__config['SID'], self.__config['token'])
        try:
            client.sms.messages.create(body=message,
                to=notification.user_to_notify.profile.phone_number,
                from_=self.__config['sms_number'])
            print 'successfully sent the sms'
        except twilio.TwilioRestException as e:
            print 'failed to send sms, Error: %s' % e
        except :
            e = sys.exc_info()[0]
            print 'failed to send sms, Error: %s' % e