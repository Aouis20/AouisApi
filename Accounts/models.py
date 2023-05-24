from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


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

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=128, null=True, blank=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserDBManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_superuser