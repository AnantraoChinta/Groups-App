from django.shortcuts import render, redirect, get_object_or_404
from base.decorators import logged_in
import json
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from django.db.models import Q


from users.models import CustomUser

# from .forms import FriendRequestForm
from .models import Profile, Relationship


# Create your views here.


def invites_received(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)

    result = list(map(lambda x: x.sender, qs))


    is_empty = False
    if len(result) == 0:
        is_empty = True

    context = {'qs': result, 'is_empty': is_empty}
    
    return render(request, 'tutor/invites.html', context)


# Can remove this function
def profiles_to_invite_list(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {'qs':qs}

    return render(request, 'tutor/profiles_to_invite_list.html', context)

def profiles_list(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {'qs':qs}

    return render(request, 'tutor/profiles_list.html', context)

# Maybe incorporate functionality for adding and removing friends directly from their profile

def userProfile(request, pk):
    user = CustomUser.objects.get(id=pk)
    profile = Profile.objects.get(user=user)
    profile_request_user = Profile.objects.get(user=request.user)
    group = None
    if user.groups.exists():
        group = user.groups.all()[0].name.upper()
    

    qs = Relationship.objects.invitations_received(profile_request_user)
    sent = Relationship.objects.filter(sender=profile_request_user, status='sent')

    invitations = list(map(lambda x: x.sender, qs))
    receivers = list(map(lambda x: x.receiver, sent))


    
    context = {'user': user, 'profile': profile, 'group': group,
    'receivers': receivers, 'invitations': invitations, 'profile_request_user': profile_request_user}
    return render(request, 'tutor/profile.html', context)

# Add an invitations object from userProfile
class ProfileListView(ListView):
    model = Profile
    template_name = 'tutor/profiles_list.html'
    # context_object_name = 'qs'

    def get_queryset(self):
        
        q = self.request.GET.get('q', '') 
        qs = Profile.objects.filter(Q(user__email__icontains=q) & ~Q(user__email__icontains=self.request.user.email) )

        # qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '') 
        profile = Profile.objects.filter(Q(user__email__icontains=q) & ~Q(user__email__icontains=self.request.user.email) ).first()

        context['is_empty'] = False

        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        
        request_user = Profile.objects.get(user=self.request.user)
        
        objects = Relationship.objects.invitations_received(request_user)
        sent = Relationship.objects.filter(sender=request_user, status='sent')

        # print(objects)
        context['invitations'] = list(map(lambda x: x.sender, objects))
        context['receivers'] = list(map(lambda x: x.receiver, sent))
        
        return context



def send_invitation(request):
    if request.method=='POST':
        user = request.user
        pk = request.POST.get('profile_pk')

        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='sent')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('user-profile')

def remove_from_friends(request):
    if request.method=='POST':
        user = request.user
        pk = request.POST.get('profile_pk')

        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        # A relationship that already exists where either request user was the one who
        # initially sent the request or one where someone else sent a connection to request user
        rel = Relationship.objects.filter(
            (Q(sender=sender) & Q(receiver=receiver)) | 
            (Q(sender=receiver) & Q(receiver=sender))
        )

        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('user-profile')

def accept_invitation(request):
    if request.method == "POST":
        pk = request.POST.get("profile-pk")
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'sent':
            rel.status = 'accepted'
            rel.save()
    return redirect(request.META.get('HTTP_REFERER'))

        



def decline_invitation(request):
    if request.method == "POST":
        pk = request.POST.get("profile-pk")
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('tutor:invites')

# Create a user interface to access the profiles
# Work on styling
# Incorporate a notification system
# Ensure that students can only add teachers, but teachers can add students and teachers






# class ProfileDetailView(DetailView):
#     model = Profile
#     template_name = 'tutor/detail.html'

#     # Retrieving information about the profile open
#     def get_object(self):
#         # slug = self.kwargs.get('slug')
#         # profile = Profile.objects.get(slug=slug)

#         # return profile
#         pass
        
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         profile = Profile.objects.get(user=user)

#         # Receiver relationship
#         rel_r = Relationship.objects.filter(sender=profile)
#         # Sender relationship
#         rel_s = Relationship.objects.filter(receiver=profile)

#         rel_receiver = []
#         rel_sender = []

#         for item in rel_r:
#             rel_receiver.append(item.receiver.user)
            
#         for item in rel_s:
#             rel_sender.append(item.sender.user)

#         context['rel_receiver'] = rel_receiver
#         context['rel_sender'] = rel_sender



#         return context








# @logged_in
# def tutoring(request):
#     is_teacher = request.user.groups.filter(name='teacher').exists()
#     users = None
#     if is_teacher:
#         users = CustomUser.objects.filter(groups__name = "student")
#     else:
#         users = CustomUser.objects.filter(groups__name = "teacher")

    

#     context = {'is_teacher': is_teacher, 'users': users}
#     return render(request, 'tutor/tutoring.html', context)

# @logged_in
# def confirm_request(request, pk):
#     user = CustomUser.objects.get(id=pk)


#     context = {'user':user}
#     return render(request, 'tutor/confirm.html', context)

# @logged_in
# def send_friend_request(request, to_user_id):
#     from_user = request.user.userprofile
#     to_user = UserProfile.objects.get(id=to_user_id)
    
#     # Check if a friend request already exists
#     existing_request = FriendRequest.objects.filter(from_user=from_user, to_user=to_user).first()
#     if not existing_request:
#         FriendRequest.objects.create(from_user=from_user, to_user=to_user)
    
#     return redirect('tutoring')

# def accept_friend_request(request, request_id):
#     friend_request = FriendRequest.objects.get(id=request_id)
    
#     if friend_request.to_user == request.user.userprofile:
#         friend_request.accepted = True
#         friend_request.save()
#         friend_request.from_user.friends.add(friend_request.to_user)
#         friend_request.to_user.friends.add(friend_request.from_user)
    
#     return redirect('profile', user_id=request.user.userprofile.id)




# @logged_in
# def send_tutor_request(request, *args, **kwargs):
#     user = request.user
#     payload = {}
#     print("request.method")
#     if request.method == "POST" and user.is_authenticated:
#         user_id =  request.POST.get("receiver_user_id")
#         print(user_id)
#         if user_id:
#             # receiver being the user who the reques is being sent to, while current user
#             # sends the request
#             receiver = CustomUser.objects.get(pk=user_id)
#             try:
#                 # Access all requests from current user to a given receiver
#                 tutor_requests = Request.objects.filter(sender=user, receiver=receiver)
#                 try:
#                     # Raise exception when attempting to send a request to someone who was already sent the same request
#                     for request in tutor_requests:
#                         # Until a valid request is sent, request to some user is inactive
#                         if request.is_active:
#                             raise Exception("Have already sent a request to this user")
#                         tutors_request = Request(sender=user, receiver=receiver)
#                         tutor_request.save()

#                         payload['response'] = "Tutor request sent."
#                 except Exception as e:
#                     payload['response'] = str(e)
#             # No requests were intially sent
#             except Request.DoesNotExist:
#                 tutor_request = Request(sender=user, receiver=receiver)
#                 tutor_request.save()
#                 payload['response'] = "Tutor request sent."
#             if payload['response'] == None:
#                 payload['response'] = "Something went wrong."
#         # If the user_id does not exist 
#         else:
#             payload['response'] = "Unable to send tutor request."
#     # This final else block should really never happen if the authentication is fine
#     else:
#         payload['response'] = "You are not authenticated to send tutor requests."
#     # Send response to frontend
#     return HttpResponse(json.dumps(payload), content_type="application/json")
            
