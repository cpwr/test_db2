from django.conf import settings
from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from .tasks import send_activation_email as send_email

# Create your models here.

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            password=password,
        )

        user.save(using=self._db)
        user.send_activation_email()
        return user

    def create_superuser(self, email, password):

        user = self.create_user(
            email,
            password=password,
        )
        user.is_superuser = user.confirmed = user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        max_length=140,
        unique=True,
    )
    name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    birthday = models.DateField(null=True)
    is_active = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=400, null=True)
    confirmed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    password_hash = models.CharField(max_length=400)
    country = models.CharField(max_length=140, null=True)
    city = models.CharField(max_length=140, null=True)

    class Meta:
        db_table = 'users'

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return f'{self.name} {self.last_name}'

    def get_short_name(self):
        return self.name

    def __str__(self):
        return f'Name: {self.name}; Email: {self.email}'

    def get_session_auth_hash(self):
        return self.password_hash

    def send_activation_email(self):
        if not self.confirmed:
            self.activation_key = self.generate_confirmation_token()
            self.save()
            send_email.apply_async(self)


    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(settings.SECRET_KEY, expiration)
        return s.dumps({'confirm': self.id}).decode()

    def confirm(self, token):
        s = Serializer(settings.SECRET_KEY)

        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        self.is_active = True
        return True

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=4)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
