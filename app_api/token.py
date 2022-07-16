from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken

USER = get_user_model()
def authenticate(request, username=None, password=None, **kwargs):
    if username is None:
        username = kwargs.get(USER.USERNAME_FIELD)

    case_insensitive_username_field = '{}__iexact'.format(USER.USERNAME_FIELD)
    users = USER._default_manager.filter(
        Q(**{case_insensitive_username_field: username}) | Q(email__iexact=username))

    for user in users:
        if user.check_password(password):
            return user
    if not users:
        USER().set_password(password)

class EmailTokenObtainSerializer(TokenObtainSerializer):
    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        return {}


class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data

from rest_framework_simplejwt.views import TokenObtainPairView

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer