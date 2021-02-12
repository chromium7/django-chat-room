from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_POST

from .forms import UserRegistrationForm

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


def register(request):
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