from django import forms
from allauth.account.forms import SignupForm
from .models import CustomUser

class UserRegistrationForm(SignupForm):
    email = forms.EmailField(help_text='Enter a valid email address')
    
    
    def clean(self):
        data = self.cleaned_data
        
        # Upon saving the user, add user to a group
        return data

    def save(self, request):

        user = super(UserRegistrationForm, self).save(request)
        user.save()

        return user

    # def save(self, commit=True):
    #     user = super(UserRegistrationForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()

    #     return user


