from rest_framework import serializers
from .models import Counsel

class CounselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counsel
        fields = '__all__'