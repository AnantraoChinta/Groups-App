from django.urls import path, include
from . import views
app_name = "tutor"
urlpatterns = [
    path('invites/', views.invites_received, name='invites'),
    path('all-profiles/', views.ProfileListView.as_view(), name='all-profiles'),
    path('profiles-to-invite-list/', views.profiles_to_invite_list, name='profiles-to-invite-list'),
    path('send-invite/', views.send_invitation, name='send-invite'),
    path('remove-friend/', views.remove_from_friends, name='remove-friend'),
    path('invites/accept/', views.accept_invitation, name='accept-invite'),
    path('invites/decline/', views.decline_invitation, name='decline-invite'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),

    # path('tutoring/', views.tutoring, name='tutoring'),
    # path('confirm-request/<str:pk>/', views.confirm_request, name='confirm_request'),
    # path('send-request/', views.send_tutor_request, name='send_request'),
]