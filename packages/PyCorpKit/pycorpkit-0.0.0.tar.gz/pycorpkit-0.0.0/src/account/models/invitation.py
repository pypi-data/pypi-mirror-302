import logging

from django.db import models

from src.common.models.abstract import AbstractBase

LOGGER = logging.getLogger(__name__)


class Invitation(AbstractBase):
    email = models.EmailField()
    accepted_invitation = models.BooleanField(default=False)
    accepted_time = models.DateTimeField(null=True, blank=True)
    invitation_sent = models.BooleanField(default=False)
