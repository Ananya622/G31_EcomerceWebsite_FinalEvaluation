

import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required



@csrf_protect
def submit_feedback(request):
    if request.method == "POST":
        feedback_data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'order_id': request.POST.get('order_id', ''),
            'shopping_experience': request.POST.get('shopping_experience'),
            'product_quality': request.POST.get('product_quality'),
            'liked_aspects': request.POST.getlist('liked_aspects'),
            'suggestion': request.POST.get('suggestion'),
            'purchase_frequency': request.POST.get('purchase_frequency'),
            'recommendation': request.POST.get('recommendation')
        }
        
        
        try:
            response = requests.post(
                "http://127.0.0.1:5000/api/feedback",  
                data=feedback_data
            )
            
            if response.status_code == 200:
                messages.success(request, "Feedback submitted successfully!")
                return redirect('feedback_success')
            else:
                messages.error(request, "Failed to submit feedback. Please try again.")
                return redirect('feedback_form')
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error connecting to server: {str(e)}")
            return redirect('feedback_form')
        
    return HttpResponse("Invalid request method.", status=400)


# View to render feedback form
def feedback_form(request):
    return render(request, 'feedback/feedback_form.html')

# View to display success message
def feedback_success(request):
    return render(request, 'feedback/success.html')  # Create a success page template


# views.py in Django

@login_required
def view_feedbacks(request):
    # Ensure only admin or approved brands can view feedbacks
    if not (request.user.groups.filter(name="Admin").exists() or request.user.groups.filter(name="Approved Brands").exists()):
        return HttpResponse("You do not have permission to view this page.", status=403)

    # Get feedback data from Flask API
    try:
        response = requests.get("http://127.0.0.1:5000/api/feedback")

        if response.status_code == 200:
            feedbacks = response.json()  # Expecting a list of feedbacks in JSON format
            return render(request, 'feedback/feedback_view.html', {'feedbacks': feedbacks})
        else:
            return HttpResponse("Failed to fetch feedbacks from Flask API.", status=500)
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error fetching feedbacks: {str(e)}", status=500)