from django.shortcuts import render

from .models import Room, Messages


# Create your views here.
def index(request):
    rooms = Room.objects.all()
    return render(request, "index.html", {"rooms": rooms})


def room(request, room_name):
    Room.objects.get_or_create(name=room_name)
    messages = Messages.objects.filter(room__name=room_name)
    return render(request, "room.html", {"room_name": room_name, "messages": messages})
