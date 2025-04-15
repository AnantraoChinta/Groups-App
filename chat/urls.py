from django.urls import path
from . import views
from base.views import home

# First part is the words that will be in the url to travel to a given page
# Second part is the method call to a given function in views
# Third part is the name given to our page

urlpatterns = [
    # path('', home, name='home'),
    path("<slug:slug>/", views.room, name="room"),

    # path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    # path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),
    # path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),

]
