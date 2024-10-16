from src.account.filters.roles import RoleFilter, RolePermissionFilter, UserRoleFilter
from src.account.models.permission import Permissions
from src.account.models.role import Role, RolePermission, UserRole
from src.account.permissions import perms
from src.account.serializers.roles import (
    PermissionsSerializer,
    RolePermissionSerializer,
    RoleSerializer,
    UserRoleSerializer,
)
from src.common.views.base import BaseViewSet


class RoleViewSet(BaseViewSet):
    """
    Adds ability to add, update and returns roles.
    """

    permissions = {
        "GET": [perms.ROLE_VIEW],
        "POST": [perms.ROLE_CREATE],
        "PATCH": [perms.ROLE_EDIT],
        "DELETE": [perms.ROLE_DELETE],
    }
    queryset = Role.objects.filter(active=True).order_by("name").all()
    serializer_class = RoleSerializer
    filterset_class = RoleFilter
    http_method_names = ["get", "post", "patch", "delete"]


class RolePermissionViewSet(BaseViewSet):
    """
    Used to update and assign permissions directly to roles.
    """

    permissions = {
        "POST": [perms.ROLE_CREATE],
        "PATCH": [perms.ROLE_EDIT],
        "DELETE": [perms.ROLE_DELETE],
    }
    queryset = RolePermission.objects.filter(active=True).all()
    serializer_class = RolePermissionSerializer
    filterset_class = RolePermissionFilter
    http_method_names = ["post", "patch"]


class UserRoleViewSet(BaseViewSet):
    """
    Used to update and assign users to roles.
    """

    permissions = {
        "POST": [perms.ROLE_CREATE],
        "PATCH": [perms.ROLE_EDIT],
        "DELETE": [perms.ROLE_DELETE],
    }
    queryset = UserRole.objects.filter(active=True).all()
    serializer_class = UserRoleSerializer
    filterset_class = UserRoleFilter
    http_method_names = ["post", "patch"]


class PermissionsViewSet(BaseViewSet):
    """User to return all permissions."""

    queryset = Permissions.objects.filter(active=True).order_by("name").all()
    serializer_class = PermissionsSerializer
    permissions = {
        "GET": [perms.PERMISSION_VIEW],
        "POST": [perms.PROFILE_CREATE],
        "PATCH": [perms.PROFILE_EDIT],
        "DELETE": [perms.PROFILE_DELETE],
    }
    filterset_fields = ("name",)
    http_method_names = ("get",)
