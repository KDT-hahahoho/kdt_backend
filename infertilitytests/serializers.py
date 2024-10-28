from rest_framework import serializers
from .models import Infertility

class InfertilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Infertility
        fields = '__all__'