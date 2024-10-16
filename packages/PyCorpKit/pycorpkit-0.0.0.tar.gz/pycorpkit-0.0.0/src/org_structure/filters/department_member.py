import django_filters

from src.common.filters.base import BaseFilter
from src.org_structure.models import DepartmentMembers


class DepartmentMemberFilter(BaseFilter):

    first_name = django_filters.CharFilter(
        "user__person__first_name", lookup_expr="istartswith"
    )

    class Meta:
        model = DepartmentMembers
        fields = ["id"]
