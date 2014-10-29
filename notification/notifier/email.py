__author__ = 'deathowl'

import smtplib

class EmailNotifier:
    def __init__(self, config):
        self.__config = config
    def notify(self, notification):

        gmail_user = self.__config['user']
        gmail_pwd = self.__config['password']
        FROM = self.__config['user']
        TO = [notification.user_to_notify.email]
        SUBJECT = "Openduty Incident Report [#{0}]".format(notification.incident.id)
        print SUBJECT
        TEXT =  notification.message
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.ehlo()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            print 'successfully sent the mail'
        except:
            print "failed to send mail"
