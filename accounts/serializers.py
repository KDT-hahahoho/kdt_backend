from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Couple

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'identification', 'gender', 'is_infertility']
        extra_kwargs = {
            'password': {'write_only': True} # 쓰기 전용
        }

    def create_user(self, validated_data):
        try:
            user = User(
                username=validated_data['username'],
                email=validated_data['email'],
                identification=validated_data['identification'],
                gender=validated_data['gender'],
                age=validated_data['age'],
                is_infertility=validated_data['is_infertility']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
        except ValidationError as error:
            raise serializers.ValidationError({'error': str(error)})
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("해당 이메일로 가입된 계정이 이미 있습니다.")
        return value
    
    def validate_identification(self, value):
        if User.objects.filter(identification=value).exists():
            raise serializers.ValidationError("해당 주민번호로 가입된 계정이 이미 있습니다.")
        return value
    

class CoupleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Couple
        fields = ['wife_id', 'husband_id']