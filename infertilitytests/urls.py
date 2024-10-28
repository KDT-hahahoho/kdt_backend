from django.urls import path
from . import views

app_name='infertility'
urlpatterns = [
    path('tests/', views.handle_infertility_tests),
    path('tests/<int:test_pk>/', views.inferlitily_detail)
]
