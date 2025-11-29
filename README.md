
# PlantCare 🌱 — Smart Plant Identification & Watering Assistant

**Identify your plants instantly. Never forget to water them again.**

PlantCare is an intelligent web application that combines **Deep Learning** with **Django** to help you identify houseplants from photos and automatically manage personalized watering schedules.

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

PlantCare/
├── media/                      # Uploaded plant images
│   └── plants_takri/           # User-uploaded photos
├── models/                     # Trained ML models
│   └── plantClassifier.h5      # CNN model
├── plant_care/                 # Main Django app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # Plant, Reminder, ChatHistory models
│   ├── serializers.py
│   ├── views.py                # API views + ML integration
│   ├── urls.py
│   ├── image_detection.py      # ML inference logic
│   └── calculate_watering_days.py
├── user/                       # Authentication app
│   └── urls.py, views.py
├── chat/                       # Plant chat feature
│   └── urls.py, views.py
├── plant/                      # Core plant operations
│   └── urls.py, views.py
├── plant_care_project/         # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── temp/                       # Temporary processed images
├── manage.py
└── requirements.txt

---

## API Endpoints (Protected)

| Method | Endpoint                          | Description                       |
|--------|-----------------------------------|-----------------------------------|
| POST   | `/api/plants/detect-and-save/`    | Upload image → Identify & save    |
| GET    | `/api/plants/my/`                 | List user's plants                |
| DELETE | `/api/plants/delete/<str:plant_id>/` | Remove plant                  |
| POST   | `/api/reminder/create/<str:plant_id>/` | Set reminder             |
| POST   | `/api/chat/<str:plant_id>/`       | Chat with your plant (Gemini)     |
| GET    | `/api/chat/<str:plant_id>/history/` | Get chat history               |

### Example Response – Detect & Save
```json
{
  "plant_type": "Snake Plant",
  "confidence": 0.94,
  "watering_days": 14,
  "image_url": "/media/plants_takri/snake_plant.jpg",
  "message": "Plant added successfully!"
}
```

---

## Watering Schedule Logic

| Plant Type             | Water Every (Days) |
|------------------------|------------------|
| Snake Plant            | 14–21            |
| Succulents / Cacti     | 14–21            |
| Peace Lily             | 7                |
| Monstera               | 7–10             |
| Pothos                 | 7–14             |
| Fiddle Leaf Fig        | 7–10             |

---

## Setup & Installation

```bash
git clone https://github.com/yourusername/PlantCare.git
cd PlantCare

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
