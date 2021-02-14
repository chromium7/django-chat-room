from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_POST

from .forms import UserRegistrationForm, CreateRoomForm
from .models import Room

def index(request):
    """
    Render homepage
    """
    context = {}

    if request.user.is_authenticated:
        # Display form
        context['room_form'] = CreateRoomForm()
        
        # Rooms joined and moderated
        rooms_joined = Room.objects.filter(participants=request.user)
        rooms_moderated = Room.objects.filter(moderators=request.user)
        
        context['rooms_joined'] = rooms_joined
        context['rooms_moderated'] = rooms_moderated

    # If there is any error, add to context and delete from session
    if request.session.get('msg'):
        context['msg'] = request.session['msg']
        del request.session['msg']
    
    return render(request, 'chat/index.html', context)


@require_POST
def chat_redirect(request):
    """
    Redirect user who input a room number to the corresponding chat room
    Add user to participant list
    """
    permission = False

    room_id = request.POST['room_id']
    password = request.POST['room_password']
    if not password:
        password = None
    
    if room_id:
        room = Room.objects.get(id=int(room_id))

        # Check if room exists
        if not room:
            request.session['msg'] = 'Room not found'
            return redirect('chat:home')
        
        # Check if passwords match
        if room.password == password:
            permission = True
            # Add user to participant list
            # or redirect if user is already in the list
            participants = room.participants.all()
            if request.user not in participants:
                room.participants.add(request.user)

    if permission:
        return redirect('chat:chat_room', int(room_id))
    else:
        request.session['msg'] = 'Incorrect password'
        return redirect('chat:home')


def chat_room(request, room_id):
    """
    Render chat room according to id specified
    """
    room = Room.objects.get(id=room_id)
    allowed = request.user in room.participants.all()
    if allowed:
        return render(request, 'chat/room.html', {
            'room': room
        })
    else:
        request.session['msg'] = "You do not have the permission to join the room"
        return redirect('chat:home')


@require_POST
def create_chat_room(request):
    """
    Create a new chat room
    Redirect to the new room after successful creation
    """
    form = CreateRoomForm(request.POST)
    if form.is_valid():
        # Create new room
        new_room = form.save(commit=False)
        new_room.creator = request.user
        new_room.save()
        new_room.participants.add(request.user)
        new_room.moderators.add(request.user)
        new_room.save()

        return redirect('chat:chat_room', new_room.id)
    else:
        request.session['msg'] = 'Failed to create a new room'
        return redirect('chat:home')


@require_POST
def delete_chat_room(request, room_id):
    """
    Delete chat room if current user is the creator
    """
    room = Room.objects.get(id=room_id)
    if room and room.creator == request.user:
        room.delete()
    else:
        request.session['msg'] = 'Failed to delete room'
    return redirect('chat:home')


@require_POST
def leave_chat_room(request, room_id):
    """
    Remove current user from the room's participant and moderator list
    """
    room = Room.objects.get(id=room_id)
    user = request.user

    room.participants.remove(user)
    if user in room.moderators.all():
        room.moderators.remove(user)
    
    return redirect('chat:home')


@require_POST
def kick_user(request, room_id, user_id):
    """
    Delete user from a room's participant and moderator list
    """
    room = Room.objects.get(id=room_id)
    user = User.objects.get(id=user_id)

    room.participants.remove(user)
    if user in room.moderators.all():
        room.moderators.remove(user)

    return redirect('chat:chat_room', room_id)


@require_POST
def mod_user(request, room_id, user_id):
    """
    Add user to the rooms moderator list
    """
    room = Room.objects.get(id=room_id)
    user = User.objects.get(id=user_id)

    room.moderators.add(user)

    return redirect('chat:chat_room', room_id)


@require_POST
def unmod_user(request, room_id, user_id):
    """
    Remove user from rooms moderator list
    """
    room = Room.objects.get(id=room_id)
    user = User.objects.get(id=user_id)

    room.moderators.remove(user)

    return redirect('chat:chat_room', room_id)


def register(request):
    """
    Create an account when post request is received
    Render registration page when get request is received
    """
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create new user instance
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            return redirect(reverse('chat:login'))
    else:
        user_form = UserRegistrationForm()

    return render(request, 'registration/register.html', {
        'user_form': user_form,
    })