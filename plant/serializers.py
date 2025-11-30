from rest_framework import serializers
from .models import Plant, WateringReminder


class WateringReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WateringReminder
        fields = [
            "id",
            "temperature",
            "humidity",
            "sunlight",
            "last_watered",
            "watering_days",
            "next_watering_date",
            "created_at",
        ]
        read_only_fields = ["watering_days", "next_watering_date", "created_at"]


class PlantSerializer(serializers.ModelSerializer):
    watering_days = serializers.SerializerMethodField()
    next_watering_date = serializers.SerializerMethodField()

    class Meta:
        model = Plant
        fields = [
            "id",
            "plant_type",
            "image",
            "created_at",
            "watering_days",
            "next_watering_date",
        ]

    def get_watering_days(self, obj):
        reminder = obj.reminders.order_by("-created_at").first()
        return reminder.watering_days if reminder else None

    def get_next_watering_date(self, obj):
        reminder = obj.reminders.order_by("-created_at").first()
        return reminder.next_watering_date if reminder else None
