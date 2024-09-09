from django.shortcuts import render, redirect, get_object_or_404
from booking_app.models import Room,Booking
from django.http import HttpResponse



def rooms_list(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    filter_option = request.GET.get('filter', 'all')  
    rooms = Room.objects.all()

    if start_time and end_time:
        conflicting_bookings = Booking.objects.filter(
            start_time__lt=start_time,
            end_time__gt=end_time,
            status='confirmed'
        )
        occupied_rooms = conflicting_bookings.values_list('room', flat=True)

        for room in rooms:
            room.is_available = room.id not in occupied_rooms

    if filter_option == 'available' and start_time and end_time:
        rooms = [room for room in rooms if room.is_available]
    context = {
        'rooms_list': rooms,
        'start_time': start_time,
        'end_time': end_time,
        'filter_option': filter_option,
    }
    
    return render(request,template_name="booking_app/rooms_list.html",context=context)



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
        room.update_availability()
        return redirect('booking_success')
        # if booking.is_available():
        #     booking.save()
        #     room.update_availability()  # Оновлюємо доступність кімнати
        #     return redirect('booking_success')
        # else:
        #     context = {
        #         'room': room, 
        #         'error': 'Selected room is not available for the chosen period.'
        #     }
        #     return render(request, template_name="booking_app/booking_from.html", context=context)
    
        # return redirect("booking-details",pk = booking.id)
    elif request.method == "GET":
        room_id = request.GET.get('room_id')
        room = get_object_or_404(Room, pk=room_id)
        
        return render(request, template_name="booking_app/booking_form.html", context={'room': room})
        # return render(request,template_name="booking_app/booking_form.html")
    

def room_details(request,room_id):
    room = get_object_or_404(Room, pk=room_id)
    bookings = Booking.objects.filter(room=room)
    context = {
            'room': room,
            "bookings": bookings
        }
    return render(request, template_name='booking_app/room_details.html', context=context)
    # try:
    #     room =
    #     booking = Booking.objects.get(id=booking_id)
    #     context = {
    #         "booking": booking
    #     }
    #     return render(request,template_name="booking_app/booking_details.html",context=context)
    # except Booking.DoesNotExist:
    #     return HttpResponse(
    #             "This booking doesn't exist",
    #             status = 404
    #         )
    
def booking_success(request):
    return render(request, template_name="booking_app/booking_success.html")