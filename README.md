
# PlantCare 🌱 — Smart Plant Identification & Watering Assistant

**Identify your plants instantly. Never forget to water them again.**

PlantCare is an intelligent mobile application that combines **Deep Learning** with **Django** to help you identify houseplants from photos and automatically manage personalized watering schedules.

Upload a photo → Get instant identification → Add to your collection → Receive smart reminders

---

## Features

- **Plant Identification** using a custom-trained CNN model  
- **Automatic Watering Schedule** calculation based on plant species  
- **Personal Plant Collection** – your plants, securely saved per user  
- **Secure & Protected API** with authentication  
- **RESTful API** built with Django REST Framework  
- **Future-ready** for notifications, mobile app & dashboard  

---

## Tech Stack

| Component            | Technology                          |
|----------------------|-------------------------------------|
| Backend              | Django, Django REST Framework      |
| API                  | Django REST Framework              |
| Deep Learning Model  | TensorFlow / Keras (CNN)           |
| Database             | SQLite (dev) → PostgreSQL (prod)    |
| Image Processing     | Pillow, OpenCV                      |
| Authentication       | Django JWT / Session Auth           |
| Deployment           | Docker-ready, Gunicorn, Nginx       |

---

## Project Structure
```
PlantCare/
├── media/                      # Uploaded plant images
│   └── plants_takri/           # User-uploaded photos
├── models/                     # Trained ML models
│   └── plantClassifier.h5    # CNN model for plant detctions
|   └── watering_reminder_model.pkl watered model
├── plant/                 # Main Django app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # Plant, Reminder, ChatHistory models
│   ├── serializers.py
│   ├── views.py                # API views + ML integration
│   ├── urls.py                 # endpoints for plants
│   ├── image_detection.py      #image detct logic
│   └── calculate_watering_days.py # calculate the time for water
├── user/                       # user Authentication app
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # users models
│   ├── serializers.py          # data to jsons
│   ├── views.py                # API views for user auth
│   ├── urls.py                 
├── chat/                       # Plant chat feature
│   ├── models.py               # model for chats
│   └── gemini_chat.py          # generate the chat with api key of gemini
│   └── urls.py, views.py
├── plant_care/         # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── temp/                       # Temporary processed images
├── manage.py
└── requirements.txt
```
---

## API Endpoints (Protected)

| Method | Endpoint                               | Description                       |
|--------|----------------------------------------|-----------------------------------|
| POST   | `/api/user/create/`                     | Signup a new user                 |
| POST   | `/api/user/login/`                      | Login user                         |
| GET    | `/api/user/me/`                         | Get current user's profile data    |
| PUT    | `/api/user/update/`                     | Update current user's profile     |
| POST   | `/api/plants/detect/`                   | Upload image → Identify plant     |
| GET    | `/api/plants/my/`                       | List user's plants                |
| DELETE | `/api/plants/delete/<str:plant_id>/`   | Remove a plant                    |
| POST   | `/api/reminder/create/<str:plant_id>/` | Create a watering reminder        |
| POST   | `/api/chat/`                            | Chat with your plant (Gemini)     |
| GET    | `/api/chat/<str:plant_id>/history/`    | Retrieve chat history for a plant |

### Example Response – Detect
```json
{
    "message": "Plant detected and saved",
    "data": {
        "id": "85c98ba2-2a88-4cd9-8030-7caaa3bbda5c",
        "plant_type": "Aloe Vera",
        "image": "/media/plants/takri/test2.png",
        "created_at": "2025-11-29T12:34:56.442122Z"
    },
    "detected_as": "Aloe Vera",
    "confidence": 91.80000305175781
}
```
### My Plants
```json
[
    {
        "id": "eb05fbc9-0818-4a04-8b0c-14992810c2fc",
        "plant_type": "Snake Plant",
        "image": "/media/plants/takri/test_6qgpJ6j.png",
        "created_at": "2025-11-29T12:07:22.712247Z"
    },
    {
        "id": "85c98ba2-2a88-4cd9-8030-7caaa3bbda5c",
        "plant_type": "Aloe Vera",
        "image": "/media/plants/takri/test2.png",
        "created_at": "2025-11-29T12:34:56.442122Z"
    }
]
```
### Set the reminder

```json
{
    "message": "Reminder created",
    "data": {
        "id": "3c9bbd6e-7612-4fa3-a89c-e5cfc5d50339",
        "plant": {
            "id": "eb05fbc9-0818-4a04-8b0c-14992810c2fc",
            "plant_type": "Snake Plant",
            "image": "/media/plants/takri/test_6qgpJ6j.png",
            "created_at": "2025-11-29T12:07:22.712247Z"
        },
        "temperature": 25.5,
        "humidity": 60.0,
        "sunlight": 8.0,
        "last_watered": "2025-11-28",
        "watering_days": 19,
        "next_watering_date": "2025-12-17",
        "created_at": "2025-11-29T12:31:14.792069Z"
    }
}
```
### Chat with api 
```json
{
    "reply": "Right now, we're talking about your wonderful **Snake Plant**! How can I help you take the best care of it today?"
}
```
### History of chat
```json
{
    "plant_name": "Snake Plant",
    "history": [
        {
            "role": "user",
            "content": "what is the disease cause it",
            "time": "2025-11-29T16:04:38.671603+00:00"
        },
        {
            "role": "model",
            "content": "Oh dear! It sounds like you're concerned about a disease affecting your Snake Plant (takri).\n\nTo help me figure out what might be going on, could you please tell me a bit more about what you're seeing? For example:\n*   Are there any spots  or discoloration on the leaves of your Snake Plant (takri)? What color are they?\n*   Are the leaves looking soft, mushy, or shrivelled?\n*   Is there any white, fuzzy growth, or tiny bugs visible?\n*   Are the leaves turning yellow or brown?\n*   Is it just a small part of the plant, or is the whole Snake Plant (takri) affected?\n\nThe more details you can give me, the better I can help your Snake Plant (takri) feel better!",
            "time": "2025-11-29T16:04:41.869400+00:00"
        },
        {
            "role": "user",
            "content": "which plnts is this",
            "time": "2025-11-29T16:50:37.444911+00:00"
        },
        {
            "role": "model",
            "content": "Right now, we're talking about your wonderful **Snake Plant**! How can I help you take the best care of it today?",
            "time": "2025-11-29T16:50:40.555407+00:00"
        }
    ]
}
```

---

## Watering Schedule Logic

| Plant Type             | Water Every (Days) |
|------------------------|------------------|
| Snake Plant            | 14–21            |
| Aloe Vera              | 14–21            |

---

## Setup & Installation

```bash
git clone https://github.com/charitraa/Plant_Care_Server.git
cd Plant_Care_Server

# Create virtual environment
python -m venv venv
source venv/bin/activate    # Linux/Mac
# or
venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Server runs at: `http://127.0.0.1:8000`

---

## Future Roadmap

- Push/email notifications for watering  
- Mobile app (React Native / Flutter)  
- Interactive plant care dashboard  
- Daily care tips & disease detection  
- Community plant sharing  
- Model retraining with user data  

---

## Contributing

We love contributions!

1. Fork the repo  
2. Create your feature branch  
3. Commit your changes  
4. Open a Pull Request  

---

## License

This project is licensed under the MIT License — see LICENSE for details.

Made with love for plant parents 🌱  
⭐ Star this repo if you like it!
