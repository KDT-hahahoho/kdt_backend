from django.urls import path
from . import views

app_name='emotions'
urlpatterns = [
    path('results/', views.handle_emotion), # 감정분석내용 등록
    path('results/<int:result_pk>/', views.emotion_detail),
    path('interests/', views.handle_interest),
]
