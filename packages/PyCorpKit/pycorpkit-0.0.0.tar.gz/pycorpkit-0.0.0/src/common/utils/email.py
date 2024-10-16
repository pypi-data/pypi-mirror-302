"""Background email sending task."""

import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

LOGGER = logging.getLogger(__name__)


@shared_task(name=__name__ + ".send_email_asynchronously", ignore_result=True)
def send_email_asynchronously(
    subject="",
    plain_text="",
    html_message="",
    recipients=None,
    attachments=None,
    bcc=None,
    cc=None,
):

    from_email = settings.DEFAULT_FROM_EMAIL
    alternatives = None
    if html_message:
        alternatives = [(html_message, "text/html")]

    mail = EmailMultiAlternatives(
        subject=subject,
        body=plain_text,
        from_email=from_email,
        to=recipients,
        bcc=bcc,
        cc=cc,
        alternatives=alternatives,
    )
    if attachments:
        filename, content, mimetype = attachments[0]
        mail.attach(filename, content, mimetype)

    return mail.send()
