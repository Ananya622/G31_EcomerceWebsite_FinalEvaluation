from django.urls import path
from . import views

urlpatterns = [
    path('form/', views.feedback_form, name='feedback_form'),  # Renders the feedback form
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),  # Submits form to Flask API
    path('view-feedbacks/', views.view_feedbacks, name='view_feedbacks'),  # Displays feedback retrieved from Flask API
    path('success/', views.feedback_success, name='feedback_success'),  # Optional: thank you page after submission
]
