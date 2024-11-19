from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render
from .models import Infertility
from .serializers import InfertilitySerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='get',
    operation_description='사용자의 모든 난임척도검사 결과 조회',
    manual_parameters=[
        openapi.Parameter(
            'memberId',
            openapi.IN_QUERY,
            description='검사 결과를 조회할 사용자의 ID',
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="난임 검사 결과 조회 성공 / 가장 최신순으로 정렬됨",
            examples={
                "application/json": {
                    "success": True,
                    "result": {
                        "totalTests": [
                            {
                                "id": 2,
                                "member_id": 5,
                                "total": 70,
                                "social": 20,
                                "sexual": 15,
                                "relational": 15,
                                "refusing": 10,
                                "essential": 10,
                                "created_at": "2024-10-27T12:34:56"
                            },
                            {
                                "id": 1,
                                "member_id": 5,
                                "total": 70,
                                "social": 20,
                                "sexual": 15,
                                "relational": 15,
                                "refusing": 10,
                                "essential": 10,
                                "created_at": "2024-10-27T12:34:56"
                            }
                        ]
                    }
                }
            }
        ),
        204: openapi.Response(description="검사 결과 없음")
    }
)
@swagger_auto_schema(
    method='post',
    operation_description="난임척도검사 결과 등록 API",
    request_body=InfertilitySerializer,
    responses={
        201: openapi.Response(
            description="난임척도검사 결과 등록 성공",
            examples={
                "application/json": {
                    "success": True,
                    "result": {
                        "id": 1,
                        "member_id": 5,
                        "total": 70,
                        "social": 20,
                        "sexual": 15,
                        "relational": 15,
                        "refusing": 10,
                        "essential": 10,
                        "created_at": "2024-10-27T12:34:56"
                    }
                }
            }
        ),
        400: openapi.Response(description="유효성 검사 실패")
    }
)
@api_view(['GET', 'POST'])
def handle_infertility_tests(request):
    EMPTY_RESULT_MESSAGE = "사용자의 난임 척도 검사 결과가 없습니다."

    if request.method == 'GET':
        member_id = request.query_params.get('memberId')
        tests = Infertility.objects.filter(member_id=member_id).order_by('-created_at')
        serializer = InfertilitySerializer(tests, many=True)

        if is_empty_test_result(serializer):
            response_data = {
                "success": True,
                "message": EMPTY_RESULT_MESSAGE,
                "result": []
            }
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        
        response_data = {
            "success": True,
            "result" : {
                "totalTests": serializer.data
            }
        }
        return Response(response_data)
    
    elif request.method == 'POST':
        serializer = InfertilitySerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {
                "success": True,
                "result": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

def is_empty_test_result(serializer):
    return len(serializer.data) == 0

@swagger_auto_schema(
    method='get',
    operation_description="난임척도검사 기록 상세 조회 API",
    manual_parameters=[
        openapi.Parameter(
            'test_pk',
            openapi.IN_PATH,
            description="상세 정보를 조회할 검사 기록의 ID",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="난임척도검사 상세 조회 성공",
            examples={
                "application/json": {
                    "success": True,
                    "result": {
                        "id": 1,
                        "member_id": 5,
                        "total": 70,
                        "social": 20,
                        "sexual": 15,
                        "relational": 15,
                        "refusing": 10,
                        "essential": 10,
                        "created_at": "2024-10-27T12:34:56"
                    }
                }
            }
        ),
        404: openapi.Response(
            description="해당 검사 기록이 존재하지 않음",
            examples={
                "application/json": {
                    "error": "해당 검사 기록이 존재하지 않습니다."
                }
            }
        )
    }
)
@api_view(['GET'])
def inferlitily_detail(request, test_pk):
    member_id = request.query_params.get('member_id')
    member_test = Infertility.objects.filter(member_id=member_id).order_by('-created_at')
    if member_test.count() > 1:
        before_test = member_test[1]
    else: 
        before_test = None
    
    try:
        test = Infertility.objects.get(pk=test_pk)
    except Infertility.DoesNotExist:
        return Response({"message": "테스트 정보가 없습니다."})
    serializer = InfertilitySerializer(test)

    if before_test is None:
        return Response({
            "success": True,
            "result": {
                "current_test": serializer.data,
                "before_test": []
            }
        })
    before_test_serializer = InfertilitySerializer(before_test)

    resposne_data = {
        "success": True,
        "result": {
            "current_test": serializer.data,
            "before_test": before_test_serializer.data
        }
    }
    return Response(resposne_data, status=status.HTTP_200_OK)