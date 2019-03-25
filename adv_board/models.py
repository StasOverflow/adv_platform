from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=5000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bargain = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

