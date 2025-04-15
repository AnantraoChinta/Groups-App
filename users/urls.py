from django.urls import path, include
from . import views

# First part is the words that will be in the url to travel to a given page
# Second part is the method call to a given function in views
# Third part is the name given to the page

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    # path('register/', views.registerPage, name='register'),

]

