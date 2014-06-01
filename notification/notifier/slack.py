from slacker import Slacker

class SlackNotifier:
  def notify(self, notification):
    slack = Slacker(notification.user_to_notify.profile.slack_apikey)
    response = slack.chat.post_message(notification.user_to_notify.profile.slack_channel, notification.message)
    if not response.error:
      print "Slack message sent"
    else:
      print "Failed to send Slack message"
