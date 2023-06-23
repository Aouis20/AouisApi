from django.db import transaction
from django.utils import timezone
from rest_framework import mixins, viewsets
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView

from Accounts.models import User
from Accounts.permissions import UserPermissions

from .serializers import (
    CreateUserSerializer,
    UserSerializer,
)


class UserViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermissions,)

    def get_serializer_class(self):
        serializers = {
            "default": super().get_serializer_class(),
            "create": CreateUserSerializer,
        }
        if self.action in serializers.keys():
            return serializers[self.action]
        else:
            return serializers["default"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serialized_data = serializer(data=request.data)

        serialized_data.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                user = User(
                    email=serialized_data.validated_data["email"],
                    is_active=True,
                )
                user.set_password(serialized_data.validated_data["password"])
                user.save()

        except ValidationError as e:
            raise e
        except Exception as e:
            if isinstance(e, ValidationError):
                raise e
            print(e)
            raise APIException("Cannot create this user")

        return Response(UserSerializer(user).data)


class TokenObtainViewSet(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")

        if not email:
            raise ValidationError("Email must be valid")

        response = super().post(request, *args, **kwargs)

        user = User.objects.get(email=email)
        user.last_login = timezone.now().date()
        user.save()

        return response


class TokenVerifyViewSet(viewsets.GenericViewSet):
    permission_classes = (UserPermissions,)

    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user).data)
