from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return self.username


class Destination(models.Model):
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        unique_together = ("city", "country")


class Schedule(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedules")
    created_at = models.DateTimeField(auto_now_add=True)
    destinations = models.ManyToManyField(
        Destination,
        through="ScheduleDestination",
        blank=True,
    )


class ScheduleDestination(models.Model):
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name="schedule_destinations"
    )
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name="schedule_destinations"
    )
    order = models.PositiveIntegerField()
    date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("schedule", "order")
        ordering = ["schedule_id", "order", "id"]
