import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import PasswordResetOTP

def login_view(request):
    if request.method == 'POST':
        login_input = request.POST.get('username')
        password = request.POST.get('password')
        
        user = None
        if '@' in login_input:
            try:
                user_obj = User.objects.get(email=login_input)
                username = user_obj.username
                user = authenticate(request, username=username, password=password)
            except User.DoesNotExist:
                user = None
        else:
            user = authenticate(request, username=login_input, password=password)
            
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username/email or password'})
            
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        address = request.POST.get('address')

        # Data retain karne ke liye context dictionary
        context = {
            'username': username,
            'email': email,
            'phone': phone,
            'gender': gender,
            'dob': dob,
            'address': address
        }

        # 1. Sabhi fields required check
        if not all([username, email, password, confirm_password, phone, gender, dob, address]):
            messages.error(request, "All fields are required.")
            return render(request, 'register.html', context)

        # 2. Password matching check
        if password != confirm_password:
            messages.error(request, "Passwords Do Not Match")
            return render(request, 'register.html', context)

        # 3. Password Length & Special Character check
        if len(password) < 7 or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messages.error(request, "Password must be at least 7 characters long and include at least 1 special character.")
            return render(request, 'register.html', context)

        # 4. Username already exists check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, 'register.html', context)

        # 5. User Creation
       # 5. User Creation
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # 6. Profile creation / update fix
        Profile.objects.update_or_create(
            user=user,
            defaults={
                'mobile_number': phone,
                'gender': gender,
                'date_of_birth': dob,
                'address': address
            }
        )
        return redirect('login')
            
    return render(request, 'register.html')

@login_required(login_url='login')
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
        
    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'accounts/profile.html', context)



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            
            # Purane OTP delete kar do
            PasswordResetOTP.objects.filter(user=user).delete()
            
            # Naya OTP save karo
            PasswordResetOTP.objects.create(user=user, otp=otp)
            
            # Email bhejo
            subject = 'Password Reset OTP'
            message = f'Hi {user.username},\n\nYour OTP for password reset is: {otp}\nIt is valid for 10 minutes.'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            
            # Session mein email save karlo verification ke liye
            request.session['reset_email'] = email
            messages.success(request, 'OTP has been sent to your email.')
            return redirect('verify_otp')
            
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
            
    return render(request, 'accounts/forgot_password.html')

def verify_otp(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')
        
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        try:
            user = User.objects.get(email=email)
            otp_obj = PasswordResetOTP.objects.filter(user=user, otp=otp_input).last()
            
            if otp_obj and not otp_obj.is_expired():
                otp_obj.is_verified = True
                otp_obj.save()
                messages.success(request, 'OTP verified successfully. Please set a new password.')
                return redirect('set_new_password')
            else:
                messages.error(request, 'Invalid or expired OTP.')
        except User.DoesNotExist:
            messages.error(request, 'Something went wrong.')
            
    return render(request, 'accounts/verify_otp.html')

def set_new_password(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')
        
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            
            # Clean up session and OTPs
            PasswordResetOTP.objects.filter(user=user).delete()
            if 'reset_email' in request.session:
                del request.session['reset_email']
                
            messages.success(request, 'Password updated successfully! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            
    return render(request, 'accounts/set_new_password.html')