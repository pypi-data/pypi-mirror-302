from django.conf import settings
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created

from src.common.utils.email import send_email_asynchronously


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # TODO! add send sms message logic here for mobile
    context = {
        "full_name": reset_password_token.user.person.full_name,
        "token": reset_password_token.key,
    }

    email_html_message = render_to_string("email/user_reset_password.html", context)
    email_plaintext_message = render_to_string("email/user_reset_password.txt", context)

    send_email_asynchronously.delay(
        subject="Password Reset for {title}".format(title=settings.APP_NAME),
        plain_text=email_plaintext_message,
        html_message=email_html_message,
        recipients=[reset_password_token.user.email],
    )
