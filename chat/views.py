from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST


def index(request):
    return render(request, 'chat/index.html')


@require_POST
def chat_redirect(request):
    room_id = int(request.POST['room_id'])
    return redirect('chat:chat_room', room_id)


def chat_room(request, room_id):
    return render(request, 'chat/room.html', {
        'room_id': room_id
    })
