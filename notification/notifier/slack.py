from slacker import Slacker

class SlackNotifier:

    def __init__(self, config):
        self.__config = config
    
    def notify(self, notification):
        slack = Slacker(self.__config['apikey'])
        response = slack.chat.post_message(notification.user_to_notify.profile.slack_room_name, notification.message)
        if not response.error:
            print "Slack message sent"
        else:
            print "Failed to send Slack message"
