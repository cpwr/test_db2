from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# Create your models here.

class CustomUserManager(BaseUserManager):

    def create_user(self, email, birthday, password=None, username=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            birthday=birthday,
        )

        user.password = password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, birthday, password):

        user = self.create_user(
            email,
            password=password,
            birthday=birthday,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):

    email = models.EmailField(
        max_length=140,
        unique=True,
    )
    birthday = models.DateField(null=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
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
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    def get_session_auth_hash(self):
        return self.password_hash

    def send_activation_email(self):
        if not self.confirmed:
            self.activation_key = self.generate_confirmation_token()
            self.save()
            path_ = reverse('activate', kwargs={"code": self.activation_key})
            #  TODO: prettify this
            full_path = "http://" + "localhost:8000" + path_
            subject = 'Activate Account'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = f'Activate your account here: {full_path}'
            recipient_list = [self.email]
            html_message = (
                f'<p>Follow the link to activate your account: {full_path}</p>'
            )
            print(html_message)
            send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False,
                html_message=html_message,
            )

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(settings.SECRET_KEY, expiration)
        return s.dumps({'confirm': self.id})

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
        self.save()
        return True

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=4)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
