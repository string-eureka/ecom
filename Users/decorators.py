from django.shortcuts import redirect
from django.contrib import messages

def vendor_check(function):
    def wrapper(request, *args, **kwargs):
        if  request.user.is_authenticated and not request.user.profile_completed:
            messages.warning(request, 'Please complete your profile before perfoming this action')
            return redirect('complete-profile')
        elif request.user.is_authenticated and request.user.user_type == 'VN':
            return function(request, *args, **kwargs)
        else:
            messages.warning(request, 'You must be a vendor to access this page.')
            return redirect('login-redirect')
    return wrapper

def customer_check(function):
    def wrapper(request, *args, **kwargs):
        if  request.user.is_authenticated and not request.user.profile_completed:
            messages.warning(request, 'Please complete your profile before perfoming this action')
            return redirect('complete-profile')

        elif request.user.is_authenticated and request.user.user_type == 'CS'and not request.user.is_superuser: 
            return function(request, *args, **kwargs)
        else:
            messages.warning(request, 'You must be a customer to access this page.') 
            return redirect('login-redirect')
    return wrapper

def already_logged(function):
    def wrapper(request, *args, **kwargs):
        if  request.user.is_authenticated and not request.user.profile_completed:
            messages.warning(request, 'Please complete your profile before perfoming this action')
            return redirect('complete-profile')

        elif request.user.is_authenticated: 
            messages.warning(request, 'You must be a customer to access this page.') 
            return redirect('login-redirect')
        else:
            return function(request, *args, **kwargs)
    return wrapper

def no_profile(function):
    def wrapper(request, *args, **kwargs):
        if  request.user.is_authenticated and not request.user.profile_completed:
            messages.warning(request, 'Please complete your profile before perfoming this action')
            return redirect('complete-profile')
        elif not request.user.is_authenticated: 
            messages.warning(request, 'You must be a logged in  to access this page.') 
            return redirect('login-redirect')
        else:
            return function(request, *args, **kwargs)
    return wrapper