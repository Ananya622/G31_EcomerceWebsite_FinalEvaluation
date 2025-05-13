E-Commerce Platform: Snatchit Django Frontend with Flask API Integration
Project Overview
This repository contains a professional e-commerce platform consisting of two complementary projects:

Snatchit_django_final - A Django-based primary application
flask_final - A Flask-based API providing specific functionality

The Django application uses the Flask API for selected functionalities while maintaining its own core features. This hybrid approach leverages the strengths of both frameworks to deliver a complete e-commerce experience.
⚠️ IMPORTANT SETUP SEQUENCE ⚠️
You MUST start the Flask API server FIRST before launching the Django application. Specific Django functionalities depend on the Flask API being available to work correctly.
Repository Structure
This project consists of two separate GitHub repositories:

flask_final - Contains the Flask API for specialized functionality
Snatchit_django_final - Contains the main Django application

Setup and Installation
Step 1: Clone Both Repositories
bash# Clone the Flask API repository
git clone https://github.com/yourusername/flask_final.git

# Clone the Django application repository
git clone https://github.com/Ananya622/G31_EcomerceWebsite_FinalEvaluation.git
Step 2: Set Up and Start the Flask API (FIRST!)
bash# Navigate to the Flask project directory
cd flask_final

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


# Start the Flask API server
flask run --port=5000
⚠️ IMPORTANT: Verify that the Flask API is running successfully before proceeding. The API should be accessible at http://127.0.0.1:5000/.
Step 3: Set Up and Start the Django Application (SECOND!)
bash# Open a new terminal window/tab
# Navigate to the Django project directory
cd Snatchit_django_final

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (if needed)
python manage.py createsuperuser

# If you are using this as a normal user then just run->
python manage.py runserver

# Start the Django development server
python manage.py runserver
Integration Architecture
This project uses a hybrid architecture where:

Django handles:

Main application logic
User interface and templating
Database models and admin functionality
User authentication and session management
Most e-commerce features


Flask API provides:

Specialized data processing endpoints
Specific functionality consumed by Django
Custom services that complement Django's capabilities



Key Features

User Registration & Authentication: Complete user management system with registration page
Product Catalog: Browse and search products
Shopping Cart: Add, modify, and remove items
Order Processing: Complete checkout flow
Admin Dashboard: Comprehensive management interface
Specialized API Integration: Flask endpoints for specific functionality

Troubleshooting API Connectivity
If you encounter issues with the Django application connecting to the Flask API:

Verify the Flask API is running (check for terminal output)
Ensure the Flask API is running on the expected port (default: 5000)
Check for any CORS configuration in the Flask application
Review network requests in browser developer tools for specific errors
Verify API endpoints are correctly configured in Django settings

Development Workflow

Always start the Flask API first
Then start the Django application
Make changes to each application in its respective repository
Test integration points thoroughly after any changes

License
This project is licensed under the MIT License - see the LICENSE file for details.
Contact
Your Name - your.email@example.com
Project Links:

Django Frontend: https://github.com/Ananya622/G31_EcomerceWebsite_FinalEvaluation.git
Flask API:https://github.com/Ananya622/G31_EcomerceWebsite_FinalEvaluation.git


Note: This README specifically addresses the integration between separate Django and Flask applications. Customize the project details as needed to match your specific implementation.RetryClaude does not have the ability to run the code it generates yet.Claude can make mistakes. Please double-check responses.