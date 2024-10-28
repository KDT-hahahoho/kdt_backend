from django.contrib import admin

from .models import Emotion, Interest

# Register your models here.
admin.site.register(Emotion)
admin.site.register(Interest)