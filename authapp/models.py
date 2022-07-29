from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
import jwt
import time
import datetime
from django.conf import settings


class UserManager(BaseUserManager):
    def _create_user(self, username: str, email: str, password: str, kwargs: dict = None) -> 'User':
        if kwargs is None:
            kwargs = {}
        if not all((username, email, password)):
            raise TypeError("User must have username, email and password")

        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username: str, email: str, password: str) -> 'User':
        return self._create_user(username, email, password)

    def create_superuser(self, username, email, password):
        return self._create_user(username, email, password, kwargs={'is_staff': True})


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def token(self):
        return self.generate_jwt_token()

    def get_customer(self) -> 'Profile':
        customer, created = Profile.objects.get_or_create(defaults={'user': self})
        return customer

    def generate_jwt_token(self) -> str:
        return jwt.encode(
            payload={
                'id': int(self.pk),
                'exp': time.time() + datetime.timedelta(days=1).total_seconds()
            },
            key=settings.SECRET_KEY,
            algorithm='HS256'
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(default='https://ak.picdn.net/contributors/175852688/avatars/thumb.jpg')
    birthday = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
