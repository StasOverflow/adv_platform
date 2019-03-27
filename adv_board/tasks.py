from __future__ import absolute_import, unicode_literals
from .celery import app
from .models import Announcement
from django.utils import timezone


@app.task
def flag_expired(*args, **kwargs):
    announcements = Announcement.objects.all()
    for adv in announcements:
        if adv.is_active:
            if (adv.last_modified + timezone.timedelta(days=30)) <= timezone.now():
                adv.is_active = False
                adv.save()
