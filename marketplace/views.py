from django.shortcuts import render


# Main Page
def main(request):
    return render(request, 'marketplace/index.html')
    
# Store Page
def store(request):
    return render(request, 'marketplace/store.html')
    
    
# Login Page
def login(request):
    return render(request, 'marketplace/login.html')
       
# Register Page
def signup(request):
    return render(request, 'marketplace/register.html')
    
# About Page
def about(request):
    return render(request, 'marketplace/about-us.html')