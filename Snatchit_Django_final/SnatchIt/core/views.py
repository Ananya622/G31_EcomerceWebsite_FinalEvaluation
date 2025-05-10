
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from products.models import Product
import requests
from django.http import HttpResponse



def is_admin_or_brand(user):
    return user.groups.filter(name__in=['Admin', 'Approved Brand']).exists()


def dashboard(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name__in=['Admin', 'Approved Brand']).exists():
            return redirect('admin_dashboard')
        else:
            return redirect('home')
    return render(request, 'core/dashboard.html')

# def index(request):
#     return render(request, 'core/index.html')  # Home page for normal users

def index(request):
    if request.user.is_authenticated and is_admin_or_brand(request.user):
        return redirect('admin_dashboard')
    return render(request, 'core/index.html')


@login_required
@user_passes_test(is_admin_or_brand)
def admin_dashboard(request):
    products = Product.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'core/admin_dashboard.html', {'products': products})

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')


def about_us_view(request):
    try:
        # Call the Flask API to get rendered HTML
        response = requests.get("http://localhost:5000/api/about-us")
        response.raise_for_status()  # Raise error for bad responses
        return HttpResponse(response.text)  # Serve the HTML as-is
    except requests.RequestException as e:
        return HttpResponse("Failed to load About Us page.", status=500)

