from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserDBManager(BaseUserManager):
    def create_user(self, email, username=None, password=None):
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(email=self.normalize_email(email), is_active=True)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, username=None, password=None):
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            is_superuser=True,
            is_staff=True,
            is_admin=True,
            is_active=True,
        )

        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived_at = models.DateTimeField(default=None, null=True)

    username = models.CharField(max_length=128, null=True, blank=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    settings = models.JSONField(default=dict)

    # Contact Information (to validate on signing up)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)

    # Address
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)

    # Favoris
    favoris = models.ManyToManyField("Products.Product", blank=True)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserDBManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_full_address(self):
        address_parts = [
            self.address_line1,
            self.address_line2,
            self.city,
            self.state,
            self.postal_code,
        ]
        return ", ".join(filter(None, address_parts))
