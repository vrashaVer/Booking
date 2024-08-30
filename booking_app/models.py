from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    number = models.IntegerField()
    capacity = models.IntegerField()
    location = models.TextField()

    
    def __str__(self):
        return f"Room №{self.number} - {self.capacity}"
    
    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        ordering = ["number"]

class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bookings")
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name="bookings")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    creation_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.room}"

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Booking"
        ordering = ["start_time"]