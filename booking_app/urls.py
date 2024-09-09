from django.urls import path
from booking_app import views

urlpatterns = [
    # path("",views.index, name="index"),
    path('', views.rooms_list, name='rooms_list'),
    path('room/<int:room_id>/', views.room_details, name='room_details'),
    path('book-room/', views.book_room, name='book_room'),
    path('booking-success/', views.booking_success, name='booking_success'),
    # path("book-room/",views.book_room,name="book-room"),
    # path("booking-details/<int:pk>/",views.booking_details,name="booking-details"),
]
