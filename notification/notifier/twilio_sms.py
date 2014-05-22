__author__ = 'deathowl'

from twilio.rest import TwilioRestClient

class TwilioSmsNotifier:

    def __init__(self, config):
        self.__config = config

    def notify(self, notification):
        client = TwilioRestClient(self.__config['SID'], self.__config['token'])
        try:
            client.sms.messages.create(body=notification.message,
                to=notification.user_to_notify.profile.phone_number,
                from_=self.__config['sms_number'])
            print 'successfully sent the sms'
        except :
            print 'failed to send sms'