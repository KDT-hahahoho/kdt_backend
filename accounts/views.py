from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import render
from django.contrib.auth import authenticate
from .serializers import UserSerializer, CoupleSerializer
from django.contrib.auth import get_user_model
from .models import Couple

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



# Create your views here.
@swagger_auto_schema(
    method='post',
    operation_description="회원가입 API",
    request_body=UserSerializer,
    responses={
        201: openapi.Response(
            description="회원가입 성공",
            examples={
                "application/json": {
                    "success": True,
                    "memberId": 1,
                }
            },
        ),
        400: openapi.Response(
            description="회원가입 실패",
            examples={
                "application/json": {
                    "email": ["This field is required."],
                    "password": ["This field is required."]
                }
            },
        )
    }
)
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        response_data = {
            "success": True,
            "memberId": user.pk
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    operation_description="로그인 API",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description="로그인할 회원의 이메일"),
            'password': openapi.Schema(type=openapi.TYPE_INTEGER, description="로그인할 회원의 비밀번호")
        },
        required=['email', 'password']
    ),
    responses={201: "로그인 성공", 401: "로그인 실패"}
)
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, username=email, password=password)
    if user is not None:
        response_data = {
            "success": True,
            "result": {
                "email": user.email,
                "memberId": user.pk,
                "gender": user.gender
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@swagger_auto_schema(
    method='post',
    operation_description="부부 등록 API",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'spouseEmail': openapi.Schema(type=openapi.TYPE_STRING, description="상대 배우자의 이메일"),
            'memberId': openapi.Schema(type=openapi.TYPE_INTEGER, description="요청 회원의 ID")
        },
        required=['spouseEmail', 'memberId']
    ),
    responses={201: "부부 등록 성공", 404: "요청한 사용자 정보가 존재하지 않습니다."}
)
@swagger_auto_schema(
    method='get',
    operation_description="부부 조회 API",
    manual_parameters=[
        openapi.Parameter('memberId', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="조회할 회원의 ID")
    ],
    responses={200: "조회 성공", 404: "요청한 사용자 정보가 존재하지 않음"}
)
@api_view(['GET', 'POST'])
def register_couple(request):
    User = get_user_model()

    if request.method == 'POST':
        spouse_email = request.data.get('spouseEmail')
        member_id = request.data.get('memberId')

        try:
            requesting_user = User.objects.get(pk=member_id)
            spouse_user = User.objects.get(email=spouse_email)
        except User.DoesNotExist:
            return Response({"error": "요청한 사용자 정보가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        if requesting_user.gender == 'W':
            couple = Couple.objects.create(wife=requesting_user, husband=spouse_user)
        elif requesting_user.gender == 'M':
            couple = Couple.objects.create(wife=spouse_user, husband=requesting_user,)
        else:
            return Response({"error": "성별 정보가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CoupleSerializer(couple)
        message = {
            "success": True,
            "result": serializer.data
        }
        return Response(message, status=status.HTTP_201_CREATED)
    
    elif request.method == 'GET':
        member_id = request.query_params.get('memberId')
        try:
            member = User.objects.get(pk=member_id)
        except User.DoesNotExist:
            return Response({"error": "요청한 사용자 정보가 존재하지 않습니다."})
        
        try:
            if member.gender == 'W':
                couple = Couple.objects.get(wife=member)
            elif member.gender == 'M':
                couple = Couple.objects.get(husband=member)
        except Couple.DoesNotExist:
            return Response({
                "success": False,
                "spouseInfo": None
            }, status=status.HTTP_200_OK)
        spouse = couple.husband if couple.wife == member else couple.wife

        response_data = {
            "success": True,
            "result": {
                "spouseInfo": {
                    "name": spouse.username,
                    "email": spouse.email,
                    "gender": spouse.gender,
                }
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)