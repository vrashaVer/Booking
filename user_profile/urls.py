from django.urls import path
from user_profile import views

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('profile/add-room/', views.add_room, name='add_room'),
    path('profile/edit-room/<int:room_id>/', views.edit_room, name='edit_room'),
    path('profile/delete-room/<int:room_id>/', views.delete_room, name='delete_room'),
    path('profile/user/<int:user_id>/', views.user_detail, name='user_detail'),

]