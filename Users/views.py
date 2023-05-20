from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm,EditProfileForm
from .models import BaseUser, CustomerUser, VendorUser
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .decorators import customer_check,vendor_check

def storefront(request):
    if request.user.is_authenticated==True and not request.user.is_superuser:
        return redirect('login-redirect')
    else:
        return render(request,'Users/front.html')

def login_redirect(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'You need to login before visiting that page')
        return redirect('login')
    elif request.user.is_superuser:
        messages.warning(request,'An admin is not allowed to perform that action')
        return redirect('front')  
    elif request.user.user_type == 'CS':
        return redirect('home')
    else:
        return redirect('dashboard')
    

def registerone(request):
    return render(request, 'Users/role.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            name=form.cleaned_data.get('name')
            phone_number=form.cleaned_data.get('phone_number')
            address=form.cleaned_data.get('address')
            password=form.cleaned_data.get('password1')
            user = BaseUser.objects.create_user(
                username=username,
                email=email,
                name=name,
                phone_number=phone_number,
                address=address,
                password=password,
            )
            if request.path == '/register/customer':
                user.user_type = 'CS'  
                CustomerUser.objects.create(user=user)  

            elif request.path == '/register/vendor':
                user.user_type = 'VN'  
                VendorUser.objects.create(user=user)  
            user.save()
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'Users/register.html', {'form': form})


@login_required
def profile(request): 
    return render (request,'Users/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'Users/edit_profile.html', {'form': form})



