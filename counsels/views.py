from rest_framework.decorators import api_view
from rest_framework.views import Response
from rest_framework import status

from django.shortcuts import render
from .models import Counsel
from .serializers import CounselSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='get',
    operation_description='회원 상담 기록 전체 조회 API',
    manual_parameters=[
        openapi.Parameter(
            'member_id',
            openapi.IN_QUERY,
            description="상담 기록을 조회할 회원의 ID",
            type=openapi.TYPE_INTEGER,
            required=True,
        )
    ],
    responses={
        200: openapi.Response(
            description="회원 상담 기록 조회 성공",
            examples={
                "application/json": {
                    "success": True,
                    "result": {
                        "totalRecords": [
                            {
                                "id": 1,
                                "member_id": 5,
                                "summary": "요약 예시",
                                "tags": "#해시태그로 #구분해서 #저장",
                                "count": 1,
                                "created_at": "2024-10-27T12:34:56",
                                "updated_at": "2024-10-27T12:34:56"
                            }
                        ]
                    }
                }
            }
        ),
        204: openapi.Response(
            description="상담 기록이 없는 경우",
            examples={
                "application/json": {
                    "success": True,
                    "message": "사용자의 상담 기록이 없습니다."
                }
            }
        )
    }
)
@swagger_auto_schema(
    method='post',
    operation_description='새로운 상담 기록 등록 API',
    request_body=CounselSerializer,
    responses={
        201: openapi.Response(
            description="상담 기록 등록 성공",
            examples={
                "application/json": {
                    "success": True,
                    "result": {
                        "id": 1,
                        "member_id": 5,
                        "summary": "새로운 요약 정보",
                        "tags": "#new #tag #s",
                        "count": 1,
                        "created_at": "2024-10-27T12:34:56",
                        "updated_at": "2024-10-27T12:34:56"
                    }
                }
            }
        ),
        400: "잘못된 요청 데이터"
    }
)
@api_view(['GET', 'POST'])
def handle_counsel_record(request):
    EMPTY_RESULT_MESSAGE = "사용자의 상담 기록이 없습니다."
    if request.method == 'GET':
        member_id = request.query_params.get('member_id')
        counsels = Counsel.objects.filter(member_id=member_id)
        serializer = CounselSerializer(counsels, many=True)
        print(member_id)

        if is_empty_counsel(serializer):
            response_data = {
                "success": True,
                "message": EMPTY_RESULT_MESSAGE,
                "result": [],
            }
            return Response(response_data)
        response_data = {
            "success": True,
            "result": {
                "totalRecords": serializer.data
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = CounselSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {
                "success": True,
                "result": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)


def is_empty_counsel(serializer):
    return len(serializer.data) == 0

@swagger_auto_schema(
    method='get',
    operation_description='상담 기록 상세 조회 API',
    manual_parameters=[
        openapi.Parameter(
            'record_pk',
            openapi.IN_PATH,
            description="조회할 상담 기록의 ID",
            type=openapi.TYPE_INTEGER,
            required=True,
        )
    ],
    responses={
        200: openapi.Response(
            description="상담 기록 조회 성공",
            examples={
                "application/json": {
                    "success": True,
                    "result": {
                        "id": 1,
                        "member_id": 5, 
                        "summary": "상세 상담 기록의 요약 정보",
                        "tags": "#상세 #상담 #기록",
                        "count": 1,
                        "created_at": "2024-10-27T12:34:56",
                        "updated_at": "2024-10-27T12:34:56"

                    }
                }
            }
        ),
        404: openapi.Response(
            description="상담 기록 조회 실패",
            examples={
                "application/json": {
                    "error": "해당 상담 기록이 존재하지 않습니다."
                }
            }
        )
    }
)
@api_view(['GET'])
def record_detail(request, record_pk):
    counsel = Counsel.objects.get(pk=record_pk)
    serializer = CounselSerializer(counsel)

    response_data = {
        "success": True,
        "result": serializer.data
    }
    return Response(response_data, status=status.HTTP_200_OK)