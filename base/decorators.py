from django.http import HttpResponse
from django.shortcuts import redirect

# decorators are a function which takes in another function as a param

# As a decorator, only perform function if user is logged in
def logged_in (view_func):
    def wrapper_func(request, *args, **kwargs):
        # if user is logged in, show home page, meaning logged in successfully
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        # if user is not logged in, show login screen
        else:
            return redirect('login')

    
    return wrapper_func


# For when user is not registered
def not_registered (view_func):
    def wrapper_func(request, *args, **kwargs):
        # if user logged in but wants to access register page, send to home
        if request.user.is_authenticated:
            return redirect('home')
        
        # if user is not logged in, send to register
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func


def allowed_users(allowed_roles=[]):
    # decorator acts kind of like the wrapper
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            # Check if user is a student or teacher
            if request.user.groups.exists():
                # Whatever group current user is in
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('home')

        return wrapper_func
    return decorator        