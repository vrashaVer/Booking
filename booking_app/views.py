from django.shortcuts import render, redirect
from booking_app.models import Room,Booking
from django.http import HttpResponse


def index(request):
    context = {
        "render_string": "Hello, world",
    }
    return render(request,template_name="booking_app/index.html",context = context)

def rooms_list(request):
    rooms = Room.objects.all()
    context = {
        "rooms_list":rooms,
    }
    return render(request,template_name="booking_app/rooms_list.html",context=context)

def book_room(request):
    if request.method == "POST":
        room_number = request.POST.get("room-number")
        start_time = request.POST.get("start-time")
        end_time = request.POST.get("end-time")

        try:
            room = Room.objects.get(number=room_number)
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
        booking = Booking.objects.create(
            user = request.user,
            room = room,
            start_time = start_time,
            end_time = end_time
        )
        return redirect("booking-details",pk = booking.id)
    else:
        return render(request,template_name="booking_app/booking_form.html")
    

def booking_details(request,pk):
    try:
        booking = Booking.objects.get(id=pk)
        context = {
            "booking": booking
        }
        return render(request,template_name="booking_app/booking_details.html",context=context)
    except Booking.DoesNotExist:
        return HttpResponse(
                "This booking doesn't exist",
                status = 404
            )