from rest_framework import serializers
from .models import Emotion, Interest

class EmotionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = '__all__'

class InterestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'


class MissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ('is_complement', )