from src.account.filters.user import UserFilter
from src.account.models.user import User
from src.account.permissions import perms
from src.account.serializers.login import UserSerializer
from src.common.views.base import BaseViewSet


class UserViewSet(BaseViewSet):
    """
    Adds ability to fetch a user details.
    """

    permissions = {
        "POST": [perms.USER_CREATE],
        "PATCH": [perms.USER_EDIT],
        "DELETE": [perms.USER_DELETE],
    }
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    http_method_names = ["get"]
