from src.common.filters.base import BaseFilter
from src.common.models.organisation import Organisation, OrganisationAttachment


class OrganisationFilter(BaseFilter):
    class Meta:
        model = Organisation
        fields = "__all__"


class OrganisationAttachmentFilter(BaseFilter):
    class Meta:
        model = OrganisationAttachment
        fields = (
            "organisation",
            "attachment",
            "created",
            "updated",
        )
