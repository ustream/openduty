from notification.notifier.xmppclient import SendClient

class XmppNotifier:
    def __init__(self, config):
        self.__config = config

    def notify(self, notification):
        client = SendClient(
            self.__config['user'], self.__config['password'],
            notification.user_to_notify.email, notification.message
        )
        client.register_plugin('xep_0030') # Service Discovery
        client.register_plugin('xep_0199') # XMPP Ping

        if client.connect((self.__config['server'], self.__config['port'])):
            client.process(block=True)
            print("Done")
        else:
            # todo: error handling
            print("Unable to connect.")
