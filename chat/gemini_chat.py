# gemini_chat.py
import google.generativeai as genai
from django.conf import settings
from .models import PlantChatMessage

genai.configure(api_key=settings.GEMINI_API_KEY)
MODEL_NAME = "gemini-2.5-flash"

# Cache one model per plant (so system prompt includes plant name)
_plant_models = {}

def get_plant_chat_model(plant_name: str):
    key = plant_name.lower()
    if key not in _plant_models:
        system_prompt = f"""
        You are GreenThumb Assistant, an expert plant carer.
        You are currently helping the user take care of their **{plant_name}**.
        Always refer to the plant by name: "{plant_name}".
        Give caring, specific, friendly advice only about this {plant_name}.
        Examples:
        - "Your {plant_name} loves bright indirect light..."
        - "Water your {plant_name} when the top 2 inches of soil are dry..."
        If asked about another plant, say: "Right now we're talking about your {plant_name}! How can I help with it?"
        """
        model = genai.GenerativeModel(
            MODEL_NAME,
            system_instruction=system_prompt
        )
        _plant_models[key] = model
    return _plant_models[key]


def plant_care_chat(plant_id: int, user_message: str, user):
    from plant.models import Plant
    
    plant = Plant.objects.get(id=plant_id, user=user)
    
    # Save user message
    PlantChatMessage.objects.create(
        plant=plant,
        role="user",
        content=user_message
    )

    # Load full history for this plant
    history = [
        {"role": msg.role, "parts": [msg.content]}
        for msg in plant.messages.all()
    ]

    # Get model with plant name in system prompt
    print(plant)
    model = get_plant_chat_model(plant.plant_type)
    chat = model.start_chat(history=history[:-1])  # exclude the latest (current) message
    
    # Send message
    response = chat.send_message(user_message)

    # Save AI reply
    PlantChatMessage.objects.create(
        plant=plant,
        role="model",
        content=response.text
    )

    return response.text.strip()