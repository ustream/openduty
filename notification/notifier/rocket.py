import requests

class RocketNotifier:
    def notify(self, notification):

        try:
            payload = {
                      "text": notification.message
                    }

            response = requests.post(notification.user_to_notify.profile.rocket_webhook_url, payload)

            if response.status_code == 200:
                print "Rocket message sent"
            else:
                print "Failed to send Rocket message, API response %s " % response.status_code
        except Exception as e:
            print "Failed to send Rocket message:%s" % e
            raise
