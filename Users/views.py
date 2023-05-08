from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import BaseUser, CustomerUser, VendorUser


def home(request):
    return render(request, 'Users/home.html')


def dashboard(request):
    return render(request, 'Users/dashboard.html')


def registerone(request):
    return render(request, 'Users/role.html')


def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email=form.cleaned_data.get('email')
            phone_number=form.cleaned_data.get('phone_number')
            address=form.cleaned_data.get('address')
            user = BaseUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                phone_number=phone_number,
                address=address,
            )
            if request.path == '/register/customer':
                user.user_type = 'CS'  
                CustomerUser.objects.create(user=user)  

            elif request.path == '/register/vendor':
                user.user_type = 'VN'  
                VendorUser.objects.create(user=user)  

            user.save()

            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'Users/register.html', {'form': form})

def profile(request): #Expand to 2 different views for Customer and Vendor
    return render (request,'Users/profile.html')