from django.urls import path
from .views import *

urlpatterns = [
    path('', serviceInfo.as_view()),
    path('auth/', auth.as_view()),
]