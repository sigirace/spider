from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):
        if not user_id:
            raise ValueError("The user_id field must be set")
        user_id = self.normalize_email(user_id)
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self.create_user(user_id, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    """Users Model Definition"""

    user_id = models.EmailField(max_length=100, unique=True, primary_key=True)
    password = models.CharField(max_length=128, null=False)
    name = models.CharField(max_length=50, null=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    last_login = models.DateTimeField(
        auto_now=True, null=True, blank=True, editable=False
    )

    objects = UserManager()

    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.user_id

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "TB_USER"
