from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Redirect based on group
            if user.groups.filter(name__in=['Admin', 'Approved Brand']).exists():
                return redirect('admin_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        profile_image = request.FILES.get('profile_image')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        print("Profile image:", profile_image)


        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')

        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=full_name,
            )

            user.save()

            profile = Profile.objects.create(
                user=user,
                phone=phone,
                dob=dob,
                gender=gender,
                address=address,
                profile_image=profile_image
            )

            profile.save()

            # Assign to default group
            default_group, _ = Group.objects.get_or_create(name='Normal User')
            user.groups.add(default_group)

            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
        except Exception as e:
                messages.error(request, 'Something went wrong during registration.')
                return redirect('register')

    return render(request, 'accounts/register.html')

def logout_view(request):
    logout(request)
    return redirect('dashboard')


@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'user': request.user  # Pass the user explicitly
    })


@login_required
def edit_profile_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.email = request.POST.get('email')
        profile.phone = request.POST.get('phone')
        profile.dob = request.POST.get('dob')
        profile.gender = request.POST.get('gender')
        profile.address = request.POST.get('address')
        # profile.profile_image=request.POST.get('profile_image')

        # # Optional profile image update
        # if request.FILES.get('profile_image'):
        #     profile.profile_image = request.FILES['profile_image']
        
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']

        user.save()
        profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return render(request, 'accounts/edit_profile.html', {'profile': profile})
