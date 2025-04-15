from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group


from django.db.models import Q
from chat.models import Room, Message
from users.models import CustomUser
from .forms import RoomForm
from .decorators import logged_in, not_registered, allowed_users





@logged_in 
def home(request):

    q = request.GET.get('q', '') 

    rooms = Room.objects.filter(
        Q(name__icontains=q),
        Q(participants__email__icontains=request.user)
    ).order_by('-created')

    room_count = rooms.count()
    # If current user is a teacher, give them the ability to click on the create-room button
    has_group = request.user.groups.filter(name='teacher').exists()


    # Only display rooms that the user is currently part of
    # Access all rooms of a student class, part of user

    
    # room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context = {'rooms': rooms, 'room_count': room_count, 'has_group': has_group}

    return render(request, 'base/home.html', context)

@logged_in
@allowed_users(allowed_roles=['teacher'])
def createRoom(request):
    form = RoomForm(request.POST or None)
    # topics = Topic.objects.all()

    if request.method == 'POST':
        # topic_name = request.POST.get('topic')
        # topic, created = Topic.objects.get_or_create(name=topic_name)

        # form not redirecting properly
        # room_form.html
        if form.is_valid():
            curr_room = Room.objects.create(
                name=request.POST.get('name'),
                host=request.user
                # description=request.POST.get('description')
            )
            room = form.save(commit=False)
            curr_room.participants.add(request.user)

            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def userProfile(request, pk):

    userm = CustomUser.objects.get(id=pk)
    rooms = userm.room_set.all()
    room_messages = userm.message_set.all()

    context = {'userm': userm, 'rooms': rooms, 'room_messages': room_messages}
    return render(request, 'base/profile.html', context)

