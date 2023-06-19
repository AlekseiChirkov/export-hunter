from django.contrib.auth import get_user_model

from rest_framework import serializers


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """User model validation serializer"""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "id", "email", "password", "confirm_password",
            "first_name", "last_name"
        )

    def create(self, validated_data: dict) -> User:
        """
        Method to validate passwords confirm and create user
        """

        password = validated_data.pop("password")
        confirm_password = validated_data.pop("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords must match!")

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """User login serializer"""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class PasswordResetSerializer(serializers.Serializer):
    """User's password reset serializer"""

    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
