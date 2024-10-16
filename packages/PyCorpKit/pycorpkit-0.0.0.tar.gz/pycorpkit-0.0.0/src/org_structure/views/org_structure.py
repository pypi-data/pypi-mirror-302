from src.account.permissions import perms
from src.common.views.base import BaseViewSet
from src.org_structure.filters.org_structure import BranchFilter, DepartmentFilter
from src.org_structure.models.branch import Branch
from src.org_structure.models.department import Department
from src.org_structure.serializers.orgs_serializers import (
    BranchResponseSerializer,
    DepartmentResponseSerializer,
)


class BranchViewSet(BaseViewSet):
    permissions = {
        "GET": [perms.BRANCH_VIEW],
        "PATCH": [perms.BRANCH_EDIT],
        "POST": [perms.BRANCH_CREATE],
        "DELETE": [perms.BRANCH_DELETE],
    }
    queryset = Branch.objects.filter(active=True).all()
    serializer_class = BranchResponseSerializer
    filterset_class = BranchFilter
    http_method_names = ["get", "post", "patch", "options"]


class DepartmentViewSet(BaseViewSet):
    permissions = {
        "GET": [perms.DEPARTMENT_VIEW],
        "PATCH": [perms.DEPARTMENT_EDIT],
        "POST": [perms.DEPARTMENT_CREATE],
        "DELETE": [perms.DEPARTMENT_DELETE],
    }
    queryset = Department.objects.filter(active=True).all()
    serializer_class = DepartmentResponseSerializer
    filterset_class = DepartmentFilter
    http_method_names = ["get", "post", "patch", "options"]
