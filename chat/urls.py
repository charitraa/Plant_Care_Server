from django.urls import path
from .views import PlantChatHistoryView, PlantChatView 

urlpatterns = [
# urls.py
path('', PlantChatView.as_view(), name='plant-chat'),
path('<str:plant_id>/history/', PlantChatHistoryView.as_view(), name='plant-chat-history'),
] 