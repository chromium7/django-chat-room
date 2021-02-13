from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_POST

from .forms import UserRegistrationForm, CreateRoomForm

def index(request):
    """
    Render homepage
    """
    context = {}

    # If there is any error, add to context and delete from session
    if request.get('msg', None):
        context['msg'] = request['msg']
        del request['msg']
    
    return render(request, 'chat/index.html', context)


@require_POST
def chat_redirect(request):
    """
    Redirect user who input a room number to the corresponding chat room
    """
    room_id = int(request.POST['room_id'])
    return redirect('chat:chat_room', room_id)


def chat_room(request, room_id):
    """
    Render chat room according to id specified
    """
    return render(request, 'chat/room.html', {
        'room_id': room_id
    })


@require_POST
def create_chat_room(request):
    """
    Create a new chat room
    Redirect to the new room after successful creation
    """
    room_id = 1
    form = CreateRoomForm(request.POST)
    if form.is_valid():
        # Create new room
        return redirect('chat:chat_room', room_id)
    else:
        request['msg'] = 'bruh'
        return redirect('chat:home')


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