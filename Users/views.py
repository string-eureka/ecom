from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm,EditProfileForm,UserProfileForm
from .models import BaseUser, CustomerUser, VendorUser
from django.urls import resolve
from django.contrib.auth.decorators import login_required
from .decorators import already_logged

def storefront(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('login-redirect')
    else:
        return render(request,'Users/front.html')

def login_redirect(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'You need to login before visiting that page')
        return redirect('login')
    elif request.user.is_superuser:
        return redirect('front')  
    elif request.user.user_type == 'CS':
        return redirect('home')
    else:
        return redirect('dashboard')
    
@already_logged
def registerone(request):
    return render(request, 'Users/role.html')

@already_logged
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
            if resolve(request.path_info).url_name == 'creg':
                user.user_type = 'CS'  
                CustomerUser.objects.create(user=user)  

            elif resolve(request.path_info).url_name == 'vreg':
                user.user_type = 'VN'  
                VendorUser.objects.create(user=user)  
            user.profile_completed=True
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

@login_required
def complete_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        username = request.user.username
        if form.is_valid():
            user_type = form.cleaned_data.get('user_type')
            base_user = BaseUser.objects.get(username=username)
            base_user.name = form.cleaned_data.get('name')
            base_user.phone_number = form.cleaned_data.get('phone_number')
            base_user.address = form.cleaned_data.get('address')
            base_user.user_type = user_type
            base_user.profile_completed = True
            base_user.save()

            if user_type == 'VN':
                VendorUser.objects.create(user=base_user)
            elif user_type == 'CS':
                CustomerUser.objects.create(user=base_user)

            messages.success(request, f'You are all set to use the website')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'Users/complete_profile.html', {'form': form})
