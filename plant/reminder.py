# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from .models import Plant
from datetime import date

@shared_task
def check_watering_reminders():
    today = date.today()
    plants = Plant.objects.all()
    for plant in plants:
        if (today - plant.last_watered).days >= plant.watering_days:
            send_mail(
                "Time to water your plant!",
                f"Hey! Your {plant.name} ({plant.plant_type}) needs water today!",
                "from@plantcare.com",
                [plant.user.email],
            )
            # Optional: send push via FCM if using mobile app