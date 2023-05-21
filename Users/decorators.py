from django.shortcuts import redirect
from django.contrib import messages

def vendor_check(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'VN':
            return function(request, *args, **kwargs)
        else:
            messages.warning(request, 'You must be a vendor to access this page.')
            return redirect('login-redirect')
    return wrapper

def customer_check(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'CS'and not request.user.is_superuser: 
            return function(request, *args, **kwargs)
        else:
            messages.warning(request, 'You must be a customer to access this page.') 
            return redirect('login-redirect')
    return wrapper
