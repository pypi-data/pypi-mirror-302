from src.account.permissions import perms
from src.common.views.base import BaseViewSet
from src.org_structure.filters.department_member import DepartmentMemberFilter
from src.org_structure.models import DepartmentMembers
from src.org_structure.serializers.orgs_serializers import (
    DepartmentMemberReadSerializer,
)


class DepartmentMemberViewSet(BaseViewSet):
    permissions = {
        "GET": [perms.DEPARTMENT_VIEW],
        "PATCH": [perms.DEPARTMENT_EDIT],
        "POST": [perms.DEPARTMENT_CREATE],
        "DELETE": [perms.DEPARTMENT_DELETE],
    }
    queryset = DepartmentMembers.objects.filter(active=True).all()
    serializer_class = DepartmentMemberReadSerializer
    filterset_class = DepartmentMemberFilter
    http_method_names = ["get", "post", "patch", "options"]
