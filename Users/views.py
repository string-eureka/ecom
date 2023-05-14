from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import BaseUser, CustomerUser, VendorUser
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .decorators import customer_check,vendor_check

def storefront(request):
    return render(request,'Users/front.html')

def login_redirect(request):
    if request.user.is_authenticated==False:
        messages.warning(request,'You need to login before visiting that page')
        return redirect('login')
    elif request.user.user_type=='CS':
        return redirect(reverse_lazy('home'))
    else: 
        return redirect(reverse_lazy('dashboard'))
    

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
def profile(request): #Expand to 2 different views for Customer and Vendor
    return render (request,'Users/profile.html')



