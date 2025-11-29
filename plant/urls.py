from django.urls import path
from .views import DetectAndSavePlantView, MyPlantsView, CreateReminderView, NotificationsView, DeletePlantView

urlpatterns = [
    path('detect/', DetectAndSavePlantView.as_view(), name='upload-plant'),
    path('my/', MyPlantsView.as_view()),
    path('reminder/create/<str:plant_id>/', CreateReminderView.as_view(), name='create-reminder'),
    path('notifications/', NotificationsView.as_view(), name='notifications'),
    path('delete/<str:plant_id>/', DeletePlantView.as_view(), name='delete-plant'),
] 