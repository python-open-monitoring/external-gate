import os

import jinja2
from mailjet_rest import Client

from settings import MAILJET_API_KEY
from settings import MAILJET_API_SECRET

file_path = os.path.dirname(os.path.abspath(__file__))


class Mailer:
    def __init__(self, sender: str, recipient_list: list, subject: str = "", letter_body: str = "", mail_service: str = "mailjet", **kwargs):

        self.sender = sender
        self.recipient_list = recipient_list
        self.subject = subject
        self.letter_body = letter_body
        self.mail_service = mail_service
        self.kwargs = kwargs
        self.outcoming_mail: str = ""

    def send_email(self):

        self._template_render()

        if self.mail_service == "mailjet":
            pass
            #self._send_mailjet()

    def _template_render(self):

        templateLoader = jinja2.FileSystemLoader(searchpath=f"{file_path}")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template("mail_template.html")
        self.outcoming_mail = template.render(subject=self.subject, letter_body=self.letter_body)

    def _send_mailjet(self):

        api_key = MAILJET_API_KEY
        api_secret = MAILJET_API_SECRET
        mailjet = Client(auth=(api_key, api_secret), version="v3.1")

        data = {"Messages": [{"From": {"Email": f"{self.sender}",}, "To": [{"Email": f"{self.recipient_list}",}], "Subject": f"{self.subject}", "HTMLPart": f"{self.outcoming_mail}",}]}
        mailjet.send.create(data=data)
