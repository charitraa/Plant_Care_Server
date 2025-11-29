from rest_framework import serializers
from .models import Plant, WateringReminder

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ["id", "plant_type", "image", "created_at"]

class WateringReminderSerializer(serializers.ModelSerializer):
    plant = PlantSerializer(read_only=True)

    class Meta:
        model = WateringReminder
        fields = [
            "id",
            "plant",
            "temperature",
            "humidity",
            "sunlight",
            "last_watered",
            "watering_days",
            "next_watering_date",
            "created_at",
        ]
        read_only_fields = ["watering_days", "next_watering_date", "created_at"]
