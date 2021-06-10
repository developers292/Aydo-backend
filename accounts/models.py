from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, phone_no, password=None, **extra_fields):
        """ Create and saves a new user """
        if not phone_no:
            raise ValueError('Users must have phone number')

        user = self.model(phone_no=phone_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, phone_no, password):
        """ create and save a new superuser """
        user = self.create_user(phone_no, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_manager = True
        user.has_permission_to_view_prices = True
        user.save(using=self._db)

        return user



class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that supports using
        phone number instead of username
    """
    phone_no = models.CharField(max_length=13, unique=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    has_permission_to_view_prices = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_no'