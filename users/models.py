from django.db import models
from django.contrib.auth.models import AbstractUser
from adv_board.models import Announcement


class AdvSiteUser(AbstractUser):
    firstname = models.CharField(blank=True, max_length=90)
    lastname = models.CharField(blank=True, max_length=90)

    favored_advs = models.ManyToManyField(Announcement, related_name='favored_by')

    def __str__(self):
        return self.username
