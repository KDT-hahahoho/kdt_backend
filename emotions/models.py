from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Interest(models.Model):
    member_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    interests = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Emotion(models.Model):
    member_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mission_content = models.TextField()
    is_complement = models.BooleanField()
    interest_keyword = models.TextField()
    self_message = models.TextField()
    export_message = models.TextField()
    joy = models.IntegerField()
    sadness = models.IntegerField()
    anger = models.IntegerField()
    fear = models.IntegerField()
    surprise = models.IntegerField()
    disgust = models.IntegerField()
    total = models.IntegerField()
    social = models.IntegerField()
    sexual = models.IntegerField()
    relational = models.IntegerField()
    refusing = models.IntegerField()
    essential = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=Emotion)
def create_interest(sender, instance, created, **kwargs):
    if created:
        # interest_keyword를 기반으로 Interest 객체 생성
        interest = Interest.objects.create(
            member_id=instance.member_id,
            interests=instance.interest_keyword
        )