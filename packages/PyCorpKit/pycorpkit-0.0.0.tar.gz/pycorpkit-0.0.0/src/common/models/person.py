import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from src.common.models.abstract import AbstractBase, Contact
from src.common.utils.constants import EMAIL, PHONE_NUMBER


class GenderChoices(models.TextChoices):
    MALE = ("MALE", _("Male"))
    FEMALE = ("FEMALE", _("Female"))
    OTHER = ("OTHER", _("Other"))


class Person(AbstractBase):
    """
    A general individual record irrespective
    of a specific professional context.
    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    surname = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(
        choices=GenderChoices.choices,
        max_length=16,
        null=True,
        blank=True,
    )
    id_number = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.CharField(max_length=100, null=True, blank=True)
    organisation = None

    model_validators = ["validate_dob"]

    @property
    def phone_number(self):
        return (
            self.person_contacts.filter(person=self.pk, contact_type=PHONE_NUMBER)
            .order_by("-is_primary", "-updated")
            .first()
            .contact_value
        )

    @property
    def email(self):
        return (
            self.person_contacts.filter(person=self.pk, contact_type=EMAIL)
            .first()
            .contact_value
        )

    @property
    def full_name(self):
        fullname = f"{self.first_name} {self.last_name}"
        if self.surname:
            fullname = f"{fullname} {self.surname}"
        return fullname

    @property
    def is_bio_data_captured(self):
        return bool(self.date_of_birth and self.id_number)

    def get_full_name(self):
        return self.full_name

    def validate_dob(self):
        """Check that the DOB is less than today and less than 150 years."""
        if self.date_of_birth:
            errs = []
            max_age = 365 * 150
            delta = datetime.timedelta(days=max_age)
            if self.date_of_birth > timezone.now().date():
                errs.append(
                    ValidationError(
                        {"date_of_birth": _("Date of birth cannot be a future date")}
                    )
                )

            oldest_person = timezone.now().date() - delta
            if self.date_of_birth < oldest_person:
                errs.append(
                    ValidationError(
                        {
                            "date_of_birth": _(
                                "A person cannot be more than 150 years old."
                            )
                        }
                    )
                )

            if errs:
                raise ValidationError(errs)

    def __str__(self):
        return self.get_full_name()


class PersonContact(Contact):
    """
    Contact information for a person.
    A person can have multiple contacts
    and those contacts can be of various types.
    """

    person = models.ForeignKey(
        Person, on_delete=models.PROTECT, related_name="person_contacts"
    )

    def __str__(self):
        return " ".join([self.person.get_full_name(), self.contact_value])
