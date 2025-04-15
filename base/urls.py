from django.urls import path
from . import views

# First part is the words that will be in the url to travel to a given page
# Second part is the method call to a given function in views
# Third part is the name given to our page

urlpatterns = [
    path('home/', views.home, name='home'),
    path('create-room/', views.createRoom, name='create-room'),
    path('user-profile/<str:pk>/', views.userProfile, name='user-profile'),
]
