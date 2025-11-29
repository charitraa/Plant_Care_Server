# views.py
from rest_framework.views import APIView
from rest_framework.response import Response

from plant_care.permission import LoginRequiredPermission
from .gemini_chat import plant_care_chat
from plant.models import Plant

class PlantChatView(APIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request):
        plant_id = request.data.get("plant_id")
        message = request.data.get("message", "").strip()

        if not plant_id or not message:
            return Response({"error": "plant_id and message required"}, status=400)

        try:
            reply = plant_care_chat(
                plant_id=plant_id,
                user_message=message,
                user=request.user
            )
            return Response({"reply": reply}, status=200)

        except Plant.DoesNotExist:
            return Response({"error": "Plant not found"}, status=404)
        except Exception as e:
            return Response({"error": f"AI is sleeping on a leaf... try again!{e}"}, status=500)


class PlantChatHistoryView(APIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request, plant_id):
        try:
            plant = Plant.objects.get(id=plant_id, user=request.user)
            messages = plant.messages.all()
            history = [
                {"role": msg.role, "content": msg.content, "time": msg.created_at.isoformat()}
                for msg in messages
            ]
            return Response({
                "plant_name": plant.plant_type,
                "history": history
            })
        except Plant.DoesNotExist:
            return Response({"error": "Plant not found"}, status=404)