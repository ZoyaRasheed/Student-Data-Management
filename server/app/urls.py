from django.urls import path

from .views import *

urlpatterns = [
    path('auth/', AuthAPIView.as_view()),
    path('user/', UserAPIView.as_view()),
]