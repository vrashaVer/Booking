from django import forms
from booking_app.models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'capacity', 'location', 'price', 'is_available']