from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import Response

from .models import Emotion, Interest
from .serializers import EmotionSerializers, InterestSerializers

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='post',
    operation_description="감정기록 분석 결과 등록 API",
    request_body=EmotionSerializers,
    responses={
        201: openapi.Response(
            description="감정기록 분석 결과 등록 성공",
            examples={
                "application/json": {
                    "success": True,
                    "result": {
                        "id": 1,
                        "mission_content": "남편과 산책하기",
                        "is_complement": False,
                        "interest_keyword": "#꽃 #결혼 #아이",
                        "self_message": "내일도 화이팅",
                        "export_message": "너도 힘내",
                        "joy": 70,
                        "sadness": 10,
                        "anger": 10,
                        "fear": 1,
                        "surprise": 30,
                        "disgust": 10,
                        "total": 100,
                        "social": 10,
                        "sexual": 10,
                        "relational": 10,
                        "refusing": 10,
                        "essential": 10,
                        "member_id": 1
                    }
                }
            }
        ),
        400: openapi.Response(description="유효성 검사 실패")
    }
)
@api_view(['POST', 'GET'])
def handle_emotion(request):
    
    if request.method == 'POST':
        serializer = EmotionSerializers(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {
                "success": True,
                "result": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
    
    elif request.method == 'GET':
        member_id = request.query_params.get('member_id')
        emotion = Emotion.objects.filter(member_id=member_id).order_by('-created_at').first()

        if emotion:
            serializer = EmotionSerializers(emotion)

            response_data = {
                "success": True,
                "result": {
                    "totalRecords": serializer.data
                }
            }
        else:
            response_data = {
                "success": False,
                "message": "등록된 감정 기록이 없습니다.",
            }
        return Response(response_data, status=status.HTTP_200_OK)





@swagger_auto_schema(
    method='get',
    operation_description="감정기록 분석 결과 상세 조회 API",
    responses={
        200: openapi.Response(
            description="감정 기록 조회 성공",
            examples={
                "application/json": {
                    "success": True,
                    "result": {
                        "id": 1,
                        "mission_content": "남편과 산책하기",
                        "is_complement": False,
                        "interest_keyword": "#꽃 #결혼 #아이",
                        "self_message": "내일도 화이팅",
                        "export_message": "너도 힘내",
                        "joy": 70,
                        "sadness": 10,
                        "anger": 10,
                        "fear": 1,
                        "surprise": 30,
                        "disgust": 10,
                        "total": 100,
                        "social": 10,
                        "sexual": 10,
                        "relational": 10,
                        "refusing": 10,
                        "essential": 10,
                        "member_id": 1
                    }
                }
            }
        ),
        404: openapi.Response(description="감정 기록이 존재하지 않습니다.")
    }
)
@swagger_auto_schema(
    method='put',
    operation_description="감정기록 분석 수정 API",
    request_body=EmotionSerializers,
    responses={
        200: openapi.Response(
            description="감정 기록 업데이트 성공",
            examples={
                "application/json": {
                    "success": True,
                    "result": {
                        "id": 1,
                        "mission_content": "남편과 산책하기",
                        "is_complement": True,
                        "interest_keyword": "#꽃 #결혼 #아이",
                        "self_message": "내일도 화이팅",
                        "export_message": "너도 힘내",
                        "joy": 70,
                        "sadness": 10,
                        "anger": 10,
                        "fear": 1,
                        "surprise": 30,
                        "disgust": 10,
                        "total": 100,
                        "social": 10,
                        "sexual": 10,
                        "relational": 10,
                        "refusing": 10,
                        "essential": 10,
                        "member_id": 1
                    }
                }
            }
        ),
        400: openapi.Response(description="유효성 검사 실패")
    }
)
@api_view(['GET', 'PUT'])
def emotion_detail(request, result_pk):
    emotion = Emotion.objects.get(pk=result_pk)

    if request.method == 'GET':
        serializer = EmotionSerializers(emotion)

        response_data = {
            "success": True,
            "result": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = EmotionSerializers(emotion, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {
                "success": True,
                "result": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="특정 회원의 모든 관심사 조회 API",
    manual_parameters=[
        openapi.Parameter(
            'member_id',
            openapi.IN_QUERY,
            description="관심사를 조회할 사용자의 ID",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="관심사 조회 성공",
            examples={
                "application/json": {
                    "success": True,
                    "result": [
                        {
                            "id": 3,
                            "interests": "#이거 #어떻게 #나올라나",
                            "created_at": "2024-10-27T19:27:41.890077+09:00",
                            "member_id": 2
                        },
                        {
                            "id": 2,
                            "interests": "#배고파 #진짜 #많이",
                            "created_at": "2024-10-27T19:27:05.426330+09:00",
                            "member_id": 2
                        }
                    ]
                }
            }
        ),
        204: openapi.Response(description="등록된 관심사가 없습니다.")
    }
)
@swagger_auto_schema(
    method='post',
    operation_description="관심사 등록 API",
    request_body=InterestSerializers,
    responses={
        201: openapi.Response(
            description="관심사 생성 성공",
            examples={
                "application/json": {
                    "success": True,
                    "result": {
                        "id": 3,
                        "interests": "#이거 #어떻게 #나올라나",
                        "created_at": "2024-10-27T19:27:41.890077+09:00",
                        "member_id": 2
                    }
                }
            }
        ),
        400: openapi.Response(description="유효성 검사 실패")
    }
)
@api_view(['GET', 'POST'])
def handle_interest(request):
    EMPTY_RESULT_MESSAGE = "등록된 관심사가 없습니다."
    if request.method == 'GET':
        member_id = request.query_params.get('member_id')
        interests = Interest.objects.filter(member_id=member_id).order_by('-created_at')
        serializer = InterestSerializers(interests, many=True)

        if is_empty_interest(serializer):
            response_data = {
                "success": True,
                "message": EMPTY_RESULT_MESSAGE,
                "result": []
            }
            return Response(response_data)
        
        response_data = {
            "success": True,
            "result": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = InterestSerializers(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {
                "success": True,
                "result": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)


def is_empty_interest(serializer):
    return len(serializer.data) == 0

