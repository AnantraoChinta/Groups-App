from django.db import models
from users.models import CustomUser
from django.template.defaultfilters import slugify


from django.db.models import Q

# Create your models here.

class ProfileManager(models.Manager):
    
    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)

        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        accepted = set([])
        for rel in qs:
            if rel.status == "accepted":
                accepted.add(rel.receiver)
                accepted.add(rel.sender)

        # An available profile is one that is not already accepted
        available = [profile for profile in profiles if profile not in accepted]

        return available

        
    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=True)
    friends = models.ManyToManyField(CustomUser, related_name='friends', blank=True)


    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def get_friends(self):
        return self.friends.all()

    def get_friends_num(self):
        return self.friends.all().count()
    
    def __str__(self):
        return str(self.user)



# ('read in database', 'read by admins')
STATUS_CHOICES = {
    ('sent', 'sent'),
    ('accepted', 'accepted'),

}

class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='sent')
        return qs

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}--{self.receiver}--{self.status}"


