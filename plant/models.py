import uuid
from django.conf import settings
from django.db import models
def plant_image_path(instance, filename):
    return f"plants/{instance.user.username}/{filename}"

class Plant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="plants")
    plant_type = models.CharField(max_length=120)
    image = models.ImageField(upload_to=plant_image_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plant_type} ({self.user.username})"

class WateringReminder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="reminders")
    temperature = models.FloatField()
    humidity = models.FloatField()
    sunlight = models.FloatField()
    last_watered = models.DateField()
    watering_days = models.PositiveIntegerField()
    next_watering_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Reminder for {self.plant.plant_type} at {self.created_at.date()}"
