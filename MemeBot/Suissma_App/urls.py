
from django.urls import path
from .views import MemeAPIView

urlpatterns = [
     path('memes/', MemeAPIView.as_view(), name='memes_api'),
]





