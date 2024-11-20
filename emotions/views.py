from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import Response
from datetime import timedelta
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Emotion, Interest
from .serializers import EmotionSerializers, InterestSerializers, MissionSerializers
from accounts.models import User, Couple

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


@api_view(['GET', 'POST'])
def get_missions(request):
    # 나의 7일 동안의 'is_complement' 값
    # 내 커플의 7일 동안의 'is_complement' 값
    member_id = request.query_params.get('member_id')
    user = get_object_or_404(User, id=member_id)

    if user.gender == 'M':
        # 사용자가 남자면 배우자는 여자
        couple = get_object_or_404(Couple, husband=user)
        spouse = couple.wife
    else:
        couple = get_object_or_404(Couple, wife=user)
        spouse = couple.husband

    today = timezone.now()
    day_list = ['SUN', 'MON', 'TUE', "WED", 'THU', 'FRI', 'SAT']
    user_missions_list = {day: [] for day in day_list}
    spouse_missions_list = {day: [] for day in day_list}

    start_of_week = today - timedelta(days=today.weekday()+1)
    end_of_week = start_of_week + timedelta(days=6)    

    # 사용자의 7일간 감정 기록 중, 'is_complement'만 뽑기
    user_missions = Emotion.objects.filter(
        member_id=user, 
        created_at__range = (start_of_week, end_of_week)
    ).values('is_complement', 'created_at')

    # 배우자의 7일간 감정 기록 중, 'is_complement'만 뽑기
    spouse_missions = Emotion.objects.filter(
        member_id=spouse, 
        created_at__range = (start_of_week, end_of_week)
    ).values('is_complement', 'created_at')

    for mission in user_missions:
        # print(mission)
        created_at = mission['created_at']
        format_date = created_at.strftime('%Y-%m-%d')
        day_of_week = created_at.strftime('%a').upper()
        if day_of_week in day_list:
            user_missions_list[day_of_week].append({
                'is_complement': mission['is_complement'],
                'created_at': f"{format_date}, {day_of_week}" 
            })
    
        # 배우자 미션 데이터 요일에 맞게 짝짓기
    for mission in spouse_missions:
        # print(mission)
        created_at = mission['created_at']
        format_date = created_at.strftime('%Y-%m-%d')
        day_of_week = created_at.strftime('%a').upper() 
        if day_of_week in day_list:
            spouse_missions_list[day_of_week].append({
                'is_complement': mission['is_complement'],
                'created_at': f"{format_date}, {day_of_week}" 
            })

    # print(user_missions_list)
    # print(spouse_missions_list)

    return Response({
        'user_is_complement': user_missions_list,
        'spouse_is_complement': spouse_missions_list
    }, status=status.HTTP_200_OK)
