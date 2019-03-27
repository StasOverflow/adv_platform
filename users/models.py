from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvSiteUser(AbstractUser):
    pass
    firstname = models.CharField(blank=True, max_length=90)
    lastname = models.CharField(blank=True, max_length=90)

    def __str__(self):
        return self.username
