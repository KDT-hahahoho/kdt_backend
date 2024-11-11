from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.
class User(AbstractUser):
    identification = models.TextField(default='010101-1')
    gender = models.CharField(max_length=10, default='M')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    

class Couple(models.Model):
    wife= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='couple_wife')
    husband= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='couple_husband')

    class Meta:
        unique_together = ('wife', 'husband')

    def __str__(self):
        return f'{self.wife} & {self.husband}'