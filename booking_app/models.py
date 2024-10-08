from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Room(models.Model):
    number = models.IntegerField()
    capacity = models.IntegerField()
    location = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    is_available = models.BooleanField(default=True)

    
    def __str__(self):
        return f"{self.number} "
    
    def check_availability(self):
        now = timezone.now()
        conflicting_bookings = Booking.objects.filter(
            room=self,
            start_time__lt=now,
            end_time__gt=now,
            status='confirmed'
        )
        return not conflicting_bookings.exists()

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
    status = models.CharField(
        max_length=20, 
        choices=[('confirmed', 'Confirmed'), ('canceled', 'Canceled')], 
        default='confirmed'
    )

    def __str__(self):
        return f"{self.user.username} - {self.room} from {self.start_time} to {self.end_time}"
    
    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Booking"
        ordering = ["start_time"]