__author__ = 'deathowl'

import logging

from sleekxmpp import ClientXMPP
from sleekxmpp.xmlstream import resolver, cert
import ssl

class SendClient(ClientXMPP):
    def verify_gtalk_cert(self, raw_cert):
        hosts = resolver.get_SRV(self.boundjid.server, 5222,
                                 self.dns_service,
                                 resolver=resolver.default_resolver())
        it_is_google = False
        for host, _ in hosts:
            if host.lower().find('google.com') > -1:
                it_is_google = True

        if it_is_google:
            try:
                if cert.verify('talk.google.com', ssl.PEM_cert_to_DER_cert(raw_cert)):
                    logging.info('google cert found for %s',
                                self.boundjid.server)
                    return
            except cert.CertificateError:
                pass

        logging.error("invalid cert received for %s",
                      self.boundjid.server)

    def __init__(self, jid, password, recipient, msg):
        super(SendClient, self).__init__(jid, password)

        self.recipient = recipient
        self.msg = msg

        self.add_event_handler('session_start', self.start)
        self.add_event_handler("ssl_invalid_cert", self.ssl_invalid_cert)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.send_message(mto=self.recipient, mbody=self.msg, mtype='chat')
        self.disconnect(wait=True)

    def ssl_invalid_cert(self, raw_cert):
        self.verify_gtalk_cert(raw_cert)