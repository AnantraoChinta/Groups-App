from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import render
from django.contrib.auth.models import Group
from users.models import CustomUser




class MySocialAccount(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        email_domain = user.email.split('@')[1]
        username = user.email.split('@')[0]
        if not email_domain == "frhsd.com":
            raise ImmediateHttpResponse(render(request, 'error.html'))
        else:
            # Ensure that the user has a valid and unique username
            try:
                custom_user, created = CustomUser.objects.get_or_create(username=username, email=user.email)
            except CustomUser.MultipleObjectsReturned:
                # Handle the case where multiple users have the same username (unlikely)
                raise ImmediateHttpResponse(render(request, 'error.html'))
            
            # Set a placeholder password
            if(custom_user not in CustomUser.objects.all()):
                print("* * *  ******************* * * * *************************")
                # custom_user.save()
            else:
                print('tf')

            if user.email[0:3].isnumeric():
                group = Group.objects.get(name="student")
            # Otherwise, the user is a teacher
            else:
                group = Group.objects.get(name="teacher")


            custom_user.groups.add(group)

