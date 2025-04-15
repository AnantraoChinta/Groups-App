from django.forms import ModelForm
from chat.models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name']
    

    