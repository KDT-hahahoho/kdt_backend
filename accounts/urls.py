from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('couple/', views.register_couple),
    path('couple/data/', views.couple_data)
]

