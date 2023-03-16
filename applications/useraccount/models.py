from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True)

    objects = UserManager()

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code


class AdditionalInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='additional')
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    status = models.CharField('Статус', max_length=100, null=True, blank=True)
    about = models.TextField('О пользователе', null=True, blank=True)
    backgroung = models.ImageField(upload_to='backgrounds', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}'


