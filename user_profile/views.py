from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from booking_app.models import Booking, Room
from django.contrib.auth.models import User
from .forms import RoomForm



@login_required
def user_profile(request):
    if request.user.is_staff:  # Перевірка, чи є користувач адміністратором
        rooms = Room.objects.all()
        users = User.objects.all()  # Додано список користувачів для адміністратора
        bookings = Booking.objects.all()  # Адміністратор бачить всі бронювання
        context = {
            'rooms': rooms,
            'users': users,
            'bookings': bookings
        }
        return render(request, 'user_profile/admin_profile.html', context)
    else:
        bookings = request.user.bookings.all()
        return render(request, 'user_profile/user_profile.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    if request.user.is_staff:
        booking = get_object_or_404(Booking, id=booking_id)
    else:
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        booking.status = 'canceled'
        booking.save()
        return redirect('user_profile')
    
    return render(request, 'cancel_booking.html', {'booking': booking})
    
@login_required
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    bookings = user.bookings.all()
    context = {
        'user': user,
        'bookings': bookings
    }
    return render(request, 'user_profile/user_detail.html', context)

@login_required
def add_room(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = RoomForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('user_profile')
        else:
            form = RoomForm()
        return render(request, 'user_profile/add_room.html', {'form': form})
    else:
        return redirect('user_profile')

@login_required
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.user.is_staff:
        if request.method == 'POST':
            form = RoomForm(request.POST, instance=room)
            if form.is_valid():
                form.save()
                return redirect('user_profile')
        else:
            form = RoomForm(instance=room)
        return render(request, 'user_profile/edit_room.html', {'form': form, 'room': room})
    else:
        return redirect('user_profile')

@login_required
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.user.is_staff:
        room.delete()
        return redirect('user_profile')
    else:
        return redirect('user_profile')


