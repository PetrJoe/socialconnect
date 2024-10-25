from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from datetime import timezone
from django.core.validators import RegexValidator

User = settings.AUTH_USER_MODEL

USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'


GENDER_CHOICES = (
    ("male", 'Male'),
    ("female", 'Female')
)


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email = self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password, **extra_fields):
        '''
        Create and return a `User` with superuser (admin) permisissions.
        '''
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(email, password, is_superuser=True)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True,blank=True, verbose_name='email address')
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    gender = models.CharField(choices=GENDER_CHOICES, default='MALE', max_length=6)
    date_joined = models.DateTimeField(auto_now_add=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserAccountManager()

    def __str__(self):
        return str(self.email)

    def get_chat_partners(self):
        sent_partners = User.objects.filter(
            received_messages__sender=self
        ).distinct()
        received_partners = User.objects.filter(
            sent_messages__receiver=self
        ).distinct()
        return (sent_partners | received_partners).distinct()
