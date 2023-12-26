import re
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from Accounts.models import User


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    confirmation = serializers.CharField()

    def validate_email(self, email):
        email_reg = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        if not email or not email_reg.fullmatch(email):
            raise ValidationError("Email must be valid")

        existing_email = User.objects.filter(email=email).exists()
        if existing_email:
            raise ValidationError("Email already registered")

        return email

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate_confirmation(self, confirm):
        password = self.initial_data.get("password")
        if confirm and password:
            if confirm != password:
                raise ValidationError("Password and Confirmation do not match")

        return confirm


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]
