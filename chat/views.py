from django.shortcuts import render, redirect
from .models import Room, Message
from users.models import CustomUser
from base.decorators import logged_in

import sys


@logged_in
def room(request, slug):
    # Find the specific room
    room_name = None
    messages = None

    room = Room.objects.get(slug = slug)
    participants = room.participants.all()

    if request.user in participants:
        if room:
            room_name = room.name
            messages = Message.objects.filter(room = room.id)
    else:
        return redirect('home')


    # Sending a message
    # Will change it
    # if request.method == 'POST':
    #     message = Message.objects.create(
    #         user=request.user,
    #         room=room,
    #         body=request.POST.get('body')
    #     )
        # room.participants.add(request.user)
        # return redirect('room', pk=room.id)

    # context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    context = {'room': room, 'room_name': room_name, 'participants': participants, 'messages': messages}
    return render(request, 'chat/room.html', context)





# @logged_in
# def room(request, pk): 
#     room = Room.objects.get(id=pk)
#     room_messages = room.message_set.all()

#     participants = room.participants.all()
#     if request.user == room.host:
#         room.participants.add(room.host)
        
#     # Sending a message
#     # Will change it
#     # if request.method == 'POST':
#     #     message = Message.objects.create(
#     #         user=request.user,
#     #         room=room,
#     #         body=request.POST.get('body')
#     #     )
#     #     room.participants.add(request.user)
#     #     return redirect('room', pk=room.id)
#     context = {'room': room, 'room_messages': room_messages, 'participants': participants}
#     return render(request, 'chat/room.html', context)

# @logged_in
# def updateRoom(request, pk):
#     room = Room.objects.get(id=pk)
#     form = RoomForm(instance=room)
#     topics = Topic.objects.all()

    
#     if request.user != room.host:
#         return HttpResponse('You are not allowed here!')

#     if request.method == 'POST':
#         room.name = request.POST.get('name')
#         room.topic = topic
#         room.description = request.POST.get('description')
#         room.save()
#         return redirect('home')

#     context = {'form': form, 'topics': topics, 'room': room}
#     return render(request, 'base/room_form.html', context)

# @logged_in
# def deleteRoom(request, pk):

#     room = Room.objects.get(id=pk)
#     if request.user != room.host:
#         return HttpResponse('You are not allowed here!')
    

#     if request.method == 'POST':
#         room.delete()
#         return redirect('home')


#     return render(request, 'base/delete.html', {'obj': room})


# @logged_in
# def deleteMessage(request, pk):

#     message = Message.objects.get(id=pk)

#     if request.user != message.user:
#         return HttpResponse('You are not allowed here!')

#     if request.method == 'POST':
#         message.delete()
#         return redirect('home')


#     return render(request, 'base/delete.html', {'obj': message})