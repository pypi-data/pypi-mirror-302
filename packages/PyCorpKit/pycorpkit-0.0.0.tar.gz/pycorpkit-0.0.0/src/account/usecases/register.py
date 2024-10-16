from http import HTTPStatus

from django.conf import settings
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone

from src.account.models.user import User
from src.common.models.person import Person
from src.common.models.profile import UserProfile
from src.common.utils.email import send_email_asynchronously


def create_user(registration_data):
    email = registration_data["email"]
    password = registration_data["password"]
    userdata = {"username": email}
    user = User.objects.create_user(email=email, password=password, **userdata)
    new_user = User.objects.generate_verify_code(user.email)
    return new_user, email


def create_person(registration_data):
    email = registration_data["email"]
    first_name = registration_data.get("first_name")
    last_name = registration_data.get("last_name")
    if not first_name and not last_name:
        first_name = email
        last_name = email

    return Person.objects.create(
        first_name=first_name,
        last_name=last_name,
    )


@transaction.atomic
def create_profile(user, person):
    profile_defaults = {
        "user": user,
        "person": person,
    }

    profile = UserProfile.objects.create(**profile_defaults)
    return profile


def send_user_activation_email(user):
    print(f"verification code: {user.verify_code}")
    expiration_hours = round(
        (user.verify_code_expire - timezone.now()).total_seconds() / 3600
    )
    text_file_content = "email/signup_confirm.txt"
    html_file_content = "email/signup_confirm.html"
    msg_subject = f"Activate Your {settings.APP_NAME} Account"
    context = {
        "full_name": user.person.first_name,
        "verification_code": user.verify_code,
        "verify_code_expire": expiration_hours,
    }
    html_message = render_to_string(html_file_content, context)
    plain_message = render_to_string(text_file_content)
    send_email_asynchronously.delay(
        subject=msg_subject,
        plain_text=plain_message,
        html_message=html_message,
        recipients=[user.email],
    )


@transaction.atomic
def register_user(registration_data):
    user, _ = create_user(registration_data)
    person = create_person(registration_data)
    create_profile(user, person)
    send_user_activation_email(user)
    response_data = {"user_id": user.id}
    return response_data, HTTPStatus.CREATED
