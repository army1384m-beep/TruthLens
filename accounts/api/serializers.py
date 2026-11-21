from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from accounts.models import User

class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        trim_whitespace=True
    )

    password = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
        )

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "This email is already registered."
            )

        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as error:
            raise serializers.ValidationError(error.messages)

        return value

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "user_id",
            "email",
            "first_name",
            "last_name",
            "created_at",
        )

        read_only_fields = (
            "user_id",
            "email",
            "created_at",
        )


class LoginSerializer(TokenObtainPairSerializer):

    username_field = User.USERNAME_FIELD

    def validate(self, attrs):
        try:
            return super().validate(attrs)

        except AuthenticationFailed:
            raise AuthenticationFailed(
                "The email or password is incorrect"
            )


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    def validate_refresh(self, value):
        try:
            RefreshToken(value)
        except TokenError:
            raise serializers.ValidationError(
                "Invalid or expired refresh token."
            )

        return value

    def save(self, **kwargs):
        token = RefreshToken(self.validated_data["refresh"])
        token.blacklist()