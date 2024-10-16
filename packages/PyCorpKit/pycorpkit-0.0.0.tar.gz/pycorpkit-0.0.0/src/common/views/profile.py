from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from src.account.permissions import perms
from src.account.serializers.login import UserResponseSerializer
from src.common.filters.profile import UserProfileAttachmentFilter, UserProfileFilter
from src.common.models.person import PersonContact
from src.common.models.profile import UserProfile, UserProfileAttachment
from src.common.serializers.profile import (
    ProfileAttachmentsUploadSerializer,
    UpdateProfileInputSerializer,
    UserProfileAttachmentSerializer,
    UserProfileSerializer,
)
from src.common.usecases.profile import create_profile_attachment
from src.common.utils.constants import EMAIL, PHONE_NUMBER
from src.common.utils.helpers import format_error_response
from src.common.views.base import BaseViewSet


class UserProfileViewSet(BaseViewSet):
    permissions = {
        "DELETE": [perms.PROFILE_DELETE],
    }
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filterset_class = UserProfileFilter
    http_method_names = ["get", "post", "patch", "options"]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get("search", None)
        if search_query:
            queryset = queryset.filter(search_vector=search_query)
        return queryset

    @transaction.atomic
    @action(methods=("post",), detail=False)
    def update_user_profile(self, request, *args, **kwargs):
        data = {**request.data}
        serializer = UpdateProfileInputSerializer(
            data=data, context={"request": request}
        )
        if not serializer.is_valid():
            data, status_code = format_error_response(
                message=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST
            )
            return Response(data, status=status_code)

        data = serializer.validated_data
        user = data["user"]
        email = data.get("email")
        person = user.person
        exclude_fields = ["user", "phone_number", "email"]
        fields = [field for field in data.keys() if field not in exclude_fields]
        for field in fields:
            value = data.get(field)
            if value is not None:
                setattr(person, field, value)
        person.save()

        contacts = PersonContact.objects.filter(person=person).all()
        phone_number = data.get("phone_number")
        for contact in contacts:
            if contact.contact_type.lower() == PHONE_NUMBER and phone_number:
                contact.contact_value = phone_number
            elif contact.contact_type.lower() == EMAIL and email:
                contact.contact_value = email
            contact.save()
        # NOTE!: email should be updated last
        if email:
            user.email = email
            user.username = email
            user.save()

        data = UserResponseSerializer(request.user)
        return Response(data=data.data, status=status.HTTP_200_OK)


class UserProfileAttachmentViewSet(BaseViewSet):
    permissions = {
        "DELETE": [perms.PROFILE_DELETE],
    }
    queryset = UserProfileAttachment.objects.all()
    serializer_class = UserProfileAttachmentSerializer
    filterset_class = UserProfileAttachmentFilter
    http_method_names = ["get", "post", "patch", "options"]

    @action(methods=("post",), detail=False)
    def upload_attachment(self, request, *args, **kwargs):
        serializer = ProfileAttachmentsUploadSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        profile_attachment = create_profile_attachment(validated_data, request.user)
        response_serializer = self.get_serializer(profile_attachment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
