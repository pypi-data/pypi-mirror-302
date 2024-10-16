from django.db import transaction
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

from src.common.utils.constants import EMAIL, PHONE_NUMBER
from src.common.utils.email import send_email_asynchronously


def get_or_create_role(name, organisation):
    from src.account.models.role import Role

    role, _ = Role.objects.get_or_create(
        name=name,
        organisation=organisation,
        defaults={},
    )
    return role


def create_user_profile(user, person):
    from src.common.models.profile import UserProfile

    user_profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={"person": person, "is_organisation": True},
    )
    return user_profile


def add_user_to_a_department(department, user_profile):
    from src.org_structure.models.department import DepartmentMembers

    department_member, _ = DepartmentMembers.objects.get_or_create(
        user=user_profile,
        department=department,
        defaults={
            "organisation": department.organisation,
        },
    )
    return department_member


def create_branch_and_department(organisation):
    from src.org_structure.models.branch import Branch
    from src.org_structure.models.department import Department

    branch, _ = Branch.objects.get_or_create(
        name="Main Branch", organisation=organisation, defaults={}
    )
    department, _ = Department.objects.get_or_create(
        name="Main Department", branch=branch, organisation=organisation, defaults={}
    )
    return department


def add_permission_to_a_role(role, perm_node):
    from src.account.models.permission import Permissions
    from src.account.models.role import RolePermission

    parent_perm, _ = Permissions.objects.update_or_create(
        name=perm_node.name,
        defaults={
            "description": perm_node.description,
            "is_deprecated": perm_node.is_deprecated,
            "is_system_level": perm_node.is_system_level,
        },
    )
    RolePermission.objects.update_or_create(
        role=role,
        permission=parent_perm,
        organisation=role.organisation,
        defaults={},
    )


def create_permission_and_roles(role, permission_nodes):
    for perm_node in permission_nodes:
        if perm_node.children:
            for child in perm_node.children:
                add_permission_to_a_role(role, child)
        add_permission_to_a_role(role, perm_node)


def assign_a_role_to_a_user_profile(role, user_profile):
    from src.account.models.role import UserRole

    user_role, _ = UserRole.objects.get_or_create(
        role=role,
        user_profile=user_profile,
        organisation=role.organisation,
        defaults={},
    )
    return user_role


def create_organisation_user(email):
    from src.account.models.user import User

    password = get_random_string(length=12)
    userdata = {"username": email}
    user, _ = User.objects.get_or_create(email=email, defaults=userdata)
    user.set_password(password)
    user.is_active = True
    user.is_verified = True
    user.save()
    return user, password


def create_person(name):
    from src.common.models.person import Person

    return Person.objects.create(
        first_name=name,
        last_name=name,
    )


def create_organisation_contacts(person, phone_number, email):
    from src.common.models.person import PersonContact

    contacts = [
        PersonContact(
            created_by=person.id,
            contact_type=PHONE_NUMBER,
            contact_value=phone_number,
            is_primary=False,
            person=person,
        ),
        PersonContact(
            created_by=person.id,
            contact_type=EMAIL,
            contact_value=email,
            is_primary=True,
            person=person,
        ),
    ]
    PersonContact.objects.bulk_create(contacts)


def notify_organisation_of_activation(organisation_name, email_address, password):
    text_file_content = "email/org_signup_confirm.txt"
    html_file_content = "email/org_signup_confirm.html"
    msg_subject = "Your PropertySync360 Account Details"
    context = {
        "name": organisation_name,
        "password": password,
    }
    html_message = render_to_string(html_file_content, context)
    plain_message = render_to_string(text_file_content)
    send_email_asynchronously.delay(
        subject=msg_subject,
        plain_text=plain_message,
        html_message=html_message,
        recipients=[email_address],
    )


def create_user_and_profile(organisation):
    user, password = create_organisation_user(organisation.email_address)
    person = create_person(organisation.name)
    create_organisation_contacts(
        person, organisation.phone_number, organisation.email_address
    )
    user_profile = create_user_profile(user, person)
    return user_profile, password


def initialize_department(organisation, user_profile):
    department = create_branch_and_department(organisation)
    add_user_to_a_department(department, user_profile)
    return department


def setup_default_roles_and_permissions(organisation, user_profile, roles_and_perms):
    for role_name, permission_nodes in roles_and_perms:
        role = get_or_create_role(role_name, organisation)
        create_permission_and_roles(role, permission_nodes)
        assign_a_role_to_a_user_profile(role, user_profile)


@transaction.atomic
def initialize_organisation(organisation, roles_and_perms):
    user_profile, password = create_user_and_profile(organisation)
    initialize_department(organisation, user_profile)
    setup_default_roles_and_permissions(organisation, user_profile, roles_and_perms)
    notify_organisation_of_activation(
        organisation_name=organisation.name,
        email_address=organisation.email_address,
        password=password,
    )
