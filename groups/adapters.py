import os

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import render
from django.contrib.auth.models import Group
from users.models import CustomUser

# Only Google accounts on this domain may sign in. Set ALLOWED_EMAIL_DOMAIN in
# the environment (or .env). Left unset, every sign-in is refused, so a missing
# value fails closed rather than opening the site to any Google account.
ALLOWED_EMAIL_DOMAIN = os.environ.get("ALLOWED_EMAIL_DOMAIN", "").strip().lower()


class MySocialAccount(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        email = (user.email or "").strip().lower()

        # Require exactly one "@" and an exact domain match. This rejects a
        # missing/empty email (which used to raise IndexError) and malformed
        # addresses such as "someone@example.com@allowed-domain.test".
        parts = email.split("@")
        if (not ALLOWED_EMAIL_DOMAIN
                or len(parts) != 2
                or parts[1] != ALLOWED_EMAIL_DOMAIN):
            raise ImmediateHttpResponse(render(request, 'error.html'))

        username = parts[0]
        if not username:
            raise ImmediateHttpResponse(render(request, 'error.html'))

        # Ensure that the user has a valid and unique username
        try:
            custom_user, created = CustomUser.objects.get_or_create(
                username=username, email=email
            )
        except CustomUser.MultipleObjectsReturned:
            # Handle the case where multiple users have the same username (unlikely)
            raise ImmediateHttpResponse(render(request, 'error.html'))

        # If the first three characters of the email are numbers, the user is a
        # student. Otherwise, the user is a teacher.
        role = "student" if email[0:3].isnumeric() else "teacher"
        group, _ = Group.objects.get_or_create(name=role)

        custom_user.groups.add(group)
