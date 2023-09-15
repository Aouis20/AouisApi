from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from Accounts.models import User


class CreateUserSerializer(serializers.Serializer):
    token = serializers.CharField()
    first_name = serializers.CharField(max_length=128)
    last_name = serializers.CharField(max_length=128)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20)
    password = serializers.CharField()
    confirmation = serializers.CharField()

    def validate_first_name(self, first_name):
        if not first_name:
            raise ValidationError("First name is required")
        if not first_name.isalpha():
            raise ValidationError(
                "The first name must contain alphabetical characters only."
            )
        return first_name

    def validate_last_name(self, last_name):
        if not last_name:
            raise ValidationError("Last name is required")
        if not last_name.isalpha():
            raise ValidationError(
                "The last name must contain alphabetical characters only."
            )
        return last_name

    def validate_email(self, email):
        email = User.objects.filter(email=email).exists()
        if email:
            raise ValidationError("Email already registered")

        return email

    def validate_phone_number(self, phone_number):
        if len(phone_number) < 10:
            raise serializers.ValidationError(
                "Phone number must contain at least 10 digits."
            )

        return phone_number

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
