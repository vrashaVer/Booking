from django.shortcuts import render, redirect, get_object_or_404
from booking_app.models import Room,Booking
from django.http import HttpResponse
from django.utils import timezone
import pytz
from django.contrib.auth.decorators import login_required


def rooms_list(request):
    start_time_str = request.GET.get('start_time')
    end_time_str = request.GET.get('end_time')
    filter_option = request.GET.get('filter', 'all')  
    rooms = Room.objects.all()

    

    if start_time_str and end_time_str:
        
        try:
            start_time = timezone.datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
            end_time = timezone.datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')

            timezone_info = pytz.timezone('Europe/Kiev')
            start_time = timezone_info.localize(start_time)
            end_time = timezone_info.localize(end_time) 

        except ValueError:
            start_time = end_time = None


        conflicting_bookings = Booking.objects.filter(
            room__in=rooms,
            status='confirmed'
        ).filter(
            # Перевірка, чи є конфлікт
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        occupied_rooms = conflicting_bookings.values_list('room', flat=True)

        for room in rooms:
            room.is_available = room.id not in occupied_rooms

    if filter_option == 'available' and start_time and end_time:
        rooms = [room for room in rooms if room.is_available]
    context = {
        'rooms_list': rooms,
        'start_time': start_time_str,
        'end_time': end_time_str,
        'filter_option': filter_option,
    }
    
    return render(request,template_name="booking_app/rooms_list.html",context=context)


@login_required()
def book_room(request):
    if request.method == "POST":
        room_id = request.POST.get("room_id")
        start_time = request.POST.get("start-time")
        end_time = request.POST.get("end-time")

        try:
            room = Room.objects.get(pk=room_id)
        except ValueError:
            return HttpResponse(
                "Wrong value for room number!",
                status = 400
            )
        except Room.DoesNotExist:
            return HttpResponse(
                "This room number doesn't exist",
                status = 404
            )
        try:
            
            start_time = timezone.datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
            end_time = timezone.datetime.strptime(end_time, '%Y-%m-%dT%H:%M')

            timezone_info = pytz.timezone('UTC')  
            start_time = timezone_info.localize(start_time)
            end_time = timezone_info.localize(end_time)
        except ValueError:
            return HttpResponse(
                "Invalid date format",
                status=400
            )

        conflicting_bookings = Booking.objects.filter(
            room=room,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status='confirmed'
        )

        if conflicting_bookings.exists():
            return render(request, 'booking_app/booking_form.html', {'room': room, 'error': 'Selected room is not available for the chosen period.'})

        booking = Booking(
            user = request.user,
            room = room,
            start_time = start_time,
            end_time = end_time,
            status='confirmed'
        ).save()
        room.check_availability()
        return redirect('booking_success')
    
    else :
        room_id = request.GET.get('room_id')
        room = get_object_or_404(Room, pk=room_id)
        
        return render(request, template_name="booking_app/booking_form.html", context={'room': room})
        # return render(request,template_name="booking_app/booking_form.html")
    

def room_details(request,room_id):


    room = get_object_or_404(Room, pk=room_id)
    start_time = request.GET.get('start-time')
    end_time = request.GET.get('end-time')

    bookings = Booking.objects.filter(
        room=room,
        status='confirmed'
    ).order_by('-start_time')
    
    if start_time and end_time:
        try:
            start_time = timezone.datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
            end_time = timezone.datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
            
            conflicting_bookings = Booking.objects.filter(
                room=room,
                start_time__lt=end_time,
                end_time__gt=start_time,
                status='confirmed'
            )
            room.is_available = not conflicting_bookings.exists()
        except ValueError:
            room.is_available = True

    context = {
        'room': room,
        'bookings': bookings,
        'start_time': start_time,
        'end_time': end_time,
    }

    return render(request, 'booking_app/room_details.html', context)
 
    
def booking_success(request):
    return render(request, template_name="booking_app/booking_success.html")

