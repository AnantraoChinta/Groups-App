from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from users.models import CustomUser
import uuid

# Create your models here.


class Room(models.Model):
    # Deleting a host deletes all its associated information
    name = models.CharField(max_length=200, null=True)
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(unique=True, max_length=140)
    # Many participants in a room, and many rooms to a participant

    created = models.DateTimeField(default=timezone.now)  

    participants = models.ManyToManyField(
        CustomUser, related_name='participants', blank=True
    )
    # updated = models.DateTimeField(auto_now=True)
    # created = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     ordering = ['-updated', '-created']

    def __str__(self):
        return self.slug

    # Ensures that the url identifier stays unique
    # Turn the title of the room into an identifier
    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Room.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug,num)
            num+=1
        return unique_slug
    # Saves the room object
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)



class Message(models.Model):
    message = models.TextField(max_length=500, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.message[0:50]
