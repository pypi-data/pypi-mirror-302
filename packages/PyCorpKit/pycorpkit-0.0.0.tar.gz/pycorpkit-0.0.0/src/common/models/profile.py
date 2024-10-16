from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from src.common.models.abstract import AbstractBase
from src.common.models.attachment import Attachments
from src.common.models.person import Person


class UserProfile(AbstractBase):
    """This allows us to connect a user with a person."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="user_profile",
    )
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    is_organisation = models.BooleanField(default=False)
    search_vector = SearchVectorField(null=True)
    organisation = None

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector"]),
        ]


class UserProfileAttachment(AbstractBase):
    """
    This makes it possible to associate
    files with users.
    """

    profile = models.ForeignKey(
        UserProfile, on_delete=models.PROTECT, related_name="user_profile_attachments"
    )
    attachment = models.ForeignKey(
        Attachments,
        null=True,
        blank=True,
        related_name="attachments_profiles",
        on_delete=models.PROTECT,
    )
    organisation = None
