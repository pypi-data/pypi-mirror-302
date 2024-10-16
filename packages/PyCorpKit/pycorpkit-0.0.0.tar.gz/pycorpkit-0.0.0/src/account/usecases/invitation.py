from datetime import timedelta

import jwt
from django.conf import settings
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone

from src.account.models.invitation import Invitation
from src.common.utils.email import send_email_asynchronously


@transaction.atomic
def invite_new_user(**user_to_invite):
    email = user_to_invite.get("email")
    role = user_to_invite.get("role")
    department = user_to_invite.get("department")
    organisation = user_to_invite.get("organisation")
    profile = user_to_invite.get("profile")
    payload = {
        "email": email,
        "department_id": str(department.pk),
        "role_id": str(role.pk),
        "profile_id": str(profile.pk),
        "exp": timezone.now() + timedelta(days=settings.INVITE_CODE_DAYS_EXPIRY),
    }
    invite_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    invitation, _ = Invitation.objects.update_or_create(
        email=email,
        defaults={
            "organisation": organisation,
        },
    )
    text_file_content = "email/user_invite.txt"
    html_file_content = "email/user_invite.html"
    msg_subject = f"New User Invite For {organisation.name}"
    context = {
        "invite_url": f"{settings.SITE_CLIENT_DOMAIN}/invite/{invite_token}",
        "organisation_name": organisation.name,
    }
    html_message = render_to_string(html_file_content, context)
    plain_message = render_to_string(text_file_content)
    send_email_asynchronously.delay(
        subject=msg_subject,
        plain_text=plain_message,
        html_message=html_message,
        recipients=[email],
    )
    invitation.invitation_sent = True
    invitation.save()
    return invite_token
