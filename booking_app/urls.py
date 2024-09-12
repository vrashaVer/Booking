from django.urls import path
from booking_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.rooms_list, name='rooms_list'),
    path('room/<int:room_id>/', views.room_details, name='room_details'),
    path('book-room/', views.book_room, name='book_room'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('logout/', auth_views.LogoutView.as_view(next_page='rooms_list'), name='logout'),

]
