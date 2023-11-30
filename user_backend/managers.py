import os

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager
from rest_framework.reverse import reverse

from user_backend.signals import user_created
from user_backend.tasks import send_mail_task

from user_backend.scripts import generate_token, get_domain


class UserManager(BaseUserManager):

    def _send_confirm_link_on_mail(self, user):
        token = generate_token(pk=user.pk)
        link = get_domain() + reverse('activate-detail', args=[token])

        message = "Dear, {}. In order to activate your account folow" \
                  "this link: {}".format(user, link)

        send_mail_task.delay(
            'Confirmation email',
            message,
            'zlava.mag@gmail.com',
            [user.email])

    def _create_user(self, username, email, password, **kwargs):

        if not username:
            raise ValueError("Username is required!")

        if not email:
            raise ValueError("Email is required!")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.password = make_password(password)
        user.save(using=self._db)

        user_created.send(
            sender=user.__class__,
            instance=user
        )

        self._send_confirm_link_on_mail(user)

        return user

    def create_user(self, username, email=None, password=None, **kwargs):

        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **kwargs)

    def create_superuser(self, username, email=None, password=None, **kwargs):

        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError("is_staff for superuser should bet True!")

        if kwargs.get('is_superuser') is not True:
            raise ValueError("is_superuser for superuser should bet True!")

        return self._create_user(username, email, password, **kwargs)
