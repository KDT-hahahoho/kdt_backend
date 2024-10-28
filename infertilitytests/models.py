from django.db import models
from django.conf import settings

# Create your models here.
class Infertility(models.Model):
    member_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.IntegerField()
    social = models.IntegerField()
    sexual = models.IntegerField()
    relational = models.IntegerField()
    refusing = models.IntegerField()
    essential = models.IntegerField()
    belifs = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)