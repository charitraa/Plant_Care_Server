import os
from datetime import timedelta, date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.conf import settings
from plant_care.permission import LoginRequiredPermission
from .models import Plant, WateringReminder
from .serializers import PlantSerializer, WateringReminderSerializer
from .image_detection import predict_plant_type
from .calculate_watering_days import predict_watering_days
from rest_framework import status

class DetectAndSavePlantView(APIView):
    permission_classes = [LoginRequiredPermission]
    parser_classes = [MultiPartParser]

    def post(self, request):
        image_file = request.FILES.get("image")
        if not image_file:
            return Response({"error": "Image is required"}, status=400)

        temp_dir = os.path.join(settings.MEDIA_ROOT, "temp")
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, image_file.name)

        with open(temp_path, "wb+") as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        try:
            predicted_class, confidence = predict_plant_type(temp_path)
        except Exception as e:
            os.remove(temp_path)
            return Response({"error": f"Prediction failed: {e}"}, status=500)

        if confidence < 0.6:
            os.remove(temp_path)
            return Response({"error": "Could not identify plant confidently"}, status=400)
        if Plant.objects.filter(user=request.user, plant_type=predicted_class.replace("_", " ").title()).exists():
            os.remove(temp_path)
            return Response({"message": "You already have this plant recorded"}, status=400)

        plant = Plant.objects.create(
            user=request.user,
            plant_type=predicted_class.replace("_", " ").title(),
            image=image_file
        )

        os.remove(temp_path)
        return Response({
            "message": "Plant detected and saved",
            "data": PlantSerializer(plant).data,
            "detected_as": predicted_class.replace("_", " ").title(),
            "confidence": round(confidence * 100, 1)
        }, status=201)

class CreateReminderView(APIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request, plant_id):
        try:
            plant = Plant.objects.get(id=plant_id, user=request.user)
        except Plant.DoesNotExist:
            return Response({"error": "Plant not found"}, status=404)

        try:
            temperature = float(request.data.get("temperature"))
            humidity = float(request.data.get("humidity"))
            sunlight = float(request.data.get("sunlight"))
            last_watered_str = request.data.get("last_watered")
            last_watered = date.fromisoformat(last_watered_str)
        except Exception as e:
            return Response({"error": f"Invalid input: {e}"}, status=400)

        watering_days = predict_watering_days(
            plant_type=plant.plant_type,
            temperature=temperature,
            humidity=humidity,
            sunlight=sunlight,
            days_since_watered=(date.today() - last_watered).days
        )

        next_watering = last_watered + timedelta(days=watering_days)

        # ✅ REPLACE OLD REMINDER
        reminder, created = WateringReminder.objects.update_or_create(
            plant=plant,
            defaults={
                "temperature": temperature,
                "humidity": humidity,
                "sunlight": sunlight,
                "last_watered": last_watered,
                "watering_days": watering_days,
                "next_watering_date": next_watering,
            }
        )

        serializer = WateringReminderSerializer(reminder)
        return Response(
            {
                "message": "Reminder replaced" if not created else "Reminder created",
                "data": serializer.data
            },
            status=200 if not created else 201
        )


class NotificationsView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request):
        today = date.today()
        reminders = WateringReminder.objects.filter(
            plant__user=request.user,
            next_watering_date__lte=today
        )
        serializer = WateringReminderSerializer(reminders, many=True)
        return Response({"data": serializer.data}, status=200)
    

class MyPlantsView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request):
        plants = Plant.objects.filter(user=request.user)
        serializer = PlantSerializer(plants, many=True)
        return Response( serializer.data, status=200)
    
class DeletePlantView(APIView):
    permission_classes = [LoginRequiredPermission]

    def delete(self, request, plant_id):
        try:
            plant = Plant.objects.get(id=plant_id, user=request.user)
        except Plant.DoesNotExist:
            return Response({"error": "Plant not found"}, status=404)

        plant.delete()
        return Response({"message": "Plant deleted successfully"}, status=200)