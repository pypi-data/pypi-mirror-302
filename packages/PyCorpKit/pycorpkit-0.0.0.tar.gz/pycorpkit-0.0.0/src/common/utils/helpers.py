import phonenumbers

from src.account.permissions.perms.apps import perm_groups
from src.common.utils.exceptions import InvalidPhoneNumber


def format_error_response(*, message, status_code):
    error_message = {"detail": message}
    if isinstance(message, dict):
        consolidated_message = " ".join(
            f"{key}: {detail}" for key, value in message.items() for detail in value
        )
        error_message["detail"] = consolidated_message
    return error_message, status_code


def get_default_roles():
    return {
        "Organisation Admin": perm_groups.ORGANISATION_ADMIN,
        "Branch Admin": perm_groups.BRANCH_ADMIN,
        "Department Admin": perm_groups.DEPARTMENT_ADMIN,
        "User": perm_groups.PROFILE_ADMIN,
    }


def validate_a_phone_number(phone_number, country="KE"):
    error = "'{}' is not a valid phone number".format(phone_number)

    try:
        parsed_number = phonenumbers.parse(phone_number, country)
    except phonenumbers.phonenumberutil.NumberParseException:
        raise InvalidPhoneNumber(error)

    if not phonenumbers.is_valid_number(parsed_number):
        raise InvalidPhoneNumber(error)

    return phonenumbers.format_number(
        parsed_number, phonenumbers.PhoneNumberFormat.E164
    )
