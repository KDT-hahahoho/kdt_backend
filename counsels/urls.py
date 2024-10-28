from django.urls import path
from . import views
app_name='counsels'
urlpatterns = [
    path('records/', views.handle_counsel_record),
    path('records/<int:record_pk>/', views.record_detail)
]
