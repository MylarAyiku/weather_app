from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (
AbstractBaseUser,
BaseUserManager,
PermissionsMixin
)


class UserManger(BaseUserManager):
    """Manger for users"""
    def create_user(self, email, password=None, **extra_fields):
        """Create ,save and return  a user """
        if not email:
            raise ValueError('Users must have an email address')
        user= self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a superuser"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser,PermissionsMixin):
    """Users in the system"""
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255,blank=True)
    city = models.CharField(max_length=50, blank=True, null=True, help_text='User default city for weather')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManger()

    USERNAME_FIELD = 'email'




    def __str__(self):
        return self.username