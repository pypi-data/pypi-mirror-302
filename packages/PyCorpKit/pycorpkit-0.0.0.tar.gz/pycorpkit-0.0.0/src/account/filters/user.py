from src.account.models.invitation import Invitation
from src.account.models.user import User
from src.common.filters.base import BaseFilter


class UserFilter(BaseFilter):

    class Meta:
        model = User
        fields = ["id", "email", "is_active"]


class UserInviteFilter(BaseFilter):

    class Meta:
        model = Invitation
        fields = "__all__"
