from django.db import models
from django.utils import timezone

class Task(models.Model):
    info = models.CharField(default="", max_length=10000)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    whitelist = models.BooleanField(default=True)

class WebsiteBlock(models.Model):
    website_regex = models.CharField(default="", max_length=10000)
    task_id = models.IntegerField(default=0)