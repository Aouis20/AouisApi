from rest_framework import serializers
from Accounts.models import User
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class CreateUserSerializer(serializers.Serializer):
    token = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    confirmation = serializers.CharField()

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate_confirmation(self, confirm):
        password = self.initial_data.get("password")
        if confirm and password:
            if confirm != password:
                raise ValidationError("Password and Confirmation do not match")

        return confirm

    def validate_email(self, email):
        email = User.objects.filter(email=email).exists()
        if email:
            raise ValidationError("Email already registered")

        return email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)
