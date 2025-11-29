# 🌱 PlantCare --- Smart Plant Identification & Watering Assistant

PlantCare is a smart web application built with **Django** and **Deep
Learning** that helps you identify plants and automatically set watering
reminders.

Simply upload a photo and let the system: - 📸 Identify the plant
species using a trained CNN model\
- 📁 Save it to your personal plant collection\
- 💧 Calculate the optimal watering schedule\
- 🔔 Send reminders (future update)

------------------------------------------------------------------------

## 🚀 Features

-   📸 **Plant identification** from uploaded images\
-   🤖 **Deep learning (CNN)** model for plant classification\
-   💧 **Automatic watering day calculation** based on species\
-   👤 **User-specific plant collection**\
-   🔒 **Protected API endpoints**\
-   ⚙️ Built with **Django REST Framework**

------------------------------------------------------------------------

## 🛠 Tech Stack

  Component          Technology
  ------------------ -------------------------------
  Backend            Django, Django REST Framework
  AI Model           TensorFlow/Keras CNN model
  Database           SQLite / PostgreSQL
  Image Processing   Pillow
  Frontend           (Coming soon)

------------------------------------------------------------------------

## 📁 Project Structure

    PlantCare/
    ├── media/
    ├── plant_care/
    │   ├── models.py
    │   ├── serializers.py
    │   ├── views.py
    │   ├── urls.py
    │   └── image_detection.py
    ├── calculate_watering_days.py
    ├── models/
    └── temp/

------------------------------------------------------------------------

## 🔌 API Endpoint

### POST /api/plants/detect-and-save/

**Authentication required**

#### Request:

    image: <plant_photo.jpg>

#### Success Response:

``` json
{
  "plant_type": "Snake Plant",
  "confidence": 0.94,
  "watering_days": 14,
  "message": "Plant added successfully!"
}
```

------------------------------------------------------------------------

## 💧 Watering Schedule Logic

  Plant Type         Watering Every (Days)
  ------------------ -----------------------
  Succulents/Cacti   14--21
  Snake Plant        14--21
  Peace Lily         7
  Monstera           7--10
  Pothos             7--14
  Fiddle Leaf Fig    7--10

------------------------------------------------------------------------

## 🛠 Setup & Installation

``` bash
git clone https://github.com/yourusername/PlantCare.git
cd PlantCare
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

------------------------------------------------------------------------

## 🔮 Future Improvements

-   Notifications\
-   Mobile App\
-   Plant care tips\
-   Watering logs\
-   Dashboard\
-   Model retraining

------------------------------------------------------------------------

## 🤝 Contributing

Fork → Commit → Pull Request

------------------------------------------------------------------------

## 📄 License

MIT License

Made with ❤️ for plant lovers.
