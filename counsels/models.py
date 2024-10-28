from django.db import models
from django.conf import settings

# Create your models here.
class Counsel(models.Model):
    member_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    summary = models.TextField()
    tags = models.TextField()
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)