from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LogUser, AddUser
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import re
import json



# Main Page
def main(request):
    class iTem:
        def __init__(self, title, price, image, category, description):
            self.title = title
            self.price = price
            self.image = image
            self.category = category
            self.description = description
    imAge = "https://static.wikia.nocookie.net/harrypotter/images/5/59/Elder_Wand.png/revision/latest?cb=20241227040818"
    class category:
        def __init__(self, title, image):
            self.title = title
            self.image = image

    class subcategory(category):
        def __init__(self, title):
            self.title = title
            #self.parent = category.title

    context = {"items": [iTem("The Elder Wand", 2000000, imAge, "Magic", "The strongest wand ever"),
                         iTem("The Elder Wand", 2000000, imAge, "Magic", "The strongest wand ever"),
                         iTem("The Elder Wand", 2000000, imAge, "Magic", "The strongest wand ever"),
                         iTem("The Elder Wand", 2000000, imAge, "Magic", "The strongest wand ever"),],
                "categories": [{"category": category("Framed Art", "/static/images/categories/framed-art.webp"), "subs": [subcategory("canvas"), subcategory("photography"), subcategory("drawing"), subcategory("vibrant")]},
                               {"category": category("Logos", "/static/images/categories/logo.avif"), "subs": [subcategory("lettermark"), subcategory("pictorial marks"), subcategory("abstract"), subcategory("mascot"), subcategory("emblem")]},
                               {"category": category("Clips", "/static/images/categories/video.webp"), "subs": [subcategory("Youtube"), subcategory("Instagram reels"), subcategory("TikTok")]},
                               {"category": category("Pictures", "/static/images/categories/picture.jpg"), "subs": [subcategory("horizantal"), subcategory("vertical"), subcategory("panoramic")]},]
                }
    return render(request, 'marketplace/index.html', context)

# Store Page
def store(request):
    return render(request, 'marketplace/store.html')

    
# Admin Page
def admin(request):
    return render(request, 'marketplace/admin.html')
    
def requests(request):
    context = {'requests': [{
                            'id': '4654',
                            'user': 'bobby',
                            'name': 'Canvas Painting',
                            'image': '',
                            'date': 'April 4, 2025',
                            'location': 'Zighoud Youcef, Constantine',
                            'category': 'A4 Canvas',
                            'status': 'pending',
                           },
                          ]
              }    
    return render(request, 'marketplace/requests.html', context)

def view_request(request, id):
    context = {'id': id}
    return render(request, 'marketplace/view_request.html', context)

def products(request):    
    return render(request, 'marketplace/products.html')


def stats(request):    
    return render(request, 'marketplace/stats.html')

def media(request):    
    return render(request, 'marketplace/media.html')

def users(request):    
    return render(request, 'marketplace/users.html')
    
def settings(request):    
    return render(request, 'marketplace/settings.html')

# Login Page
def login(request):
    return render(request, 'marketplace/login.html')
 
# About Page
def about(request):
    return render(request, 'marketplace/about-us.html')
    

# On Demand
def ondemand(request, page):
    context = {}
    with open("marketplace/static/json/Wilaya_Of_Algeria.json", "rb") as jsonFile:
        data = json.load(jsonFile)
        context['wilayas'] = data
    with open("marketplace/static/json/Commune_Of_Algeria.json", "rb") as jsonFile:
        data = json.load(jsonFile)
        context['communes'] = data
    if page == "framed":
        if request.POST:
            print(request.POST)
            return render(request, "marketplace/framed.html", context)
        else:
            return render(request, "marketplace/framed.html", context)
    else:
        return render(request, "marketplace/logo.html")

# Services
def services(request):
    return

# Login Page
def login(request):
    if request.method == "POST":
        form = LogUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Authentication
            try:
                user = User.objects.get(username=username)
                if user.password != password:
                    messages.error(request,'Invalid password')
                    return redirect("/login")
            except User.DoesNotExist:
                user = None
            # If authentication is successful Login
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"{username} Logged In Successfully!")
                return redirect("home")
            else:
                messages.error(request, "Cannot Log In!")
                return redirect("/login")
    else:
        form = LogUser()
    return render(request, 'marketplace/login.html', {'form': form})

# Register Page
def signup(request):
    if request.method == "POST":
        form = AddUser(request.POST)
        if form.is_valid():
            # Get user data from the form
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm = form.cleaned_data['confirm']
            # Check if email is valid
            email_pattern = re.compile(r'[a-z0-9_./]+@{1}[a-z0-9#]+.[a-z0-9]{2,5}')
            if re.fullmatch(email_pattern, email):
                # Check whether the password is valid
                password_pattern = re.compile(r'[A-Za-z0-9~`!@#$%^&*()_+={[}]|\:;"\'<,>.?/]+')
                if password_pattern.search(password) and len(password) >= 8:
                    # Check if the password is equal to the confirm  password
                    if password == confirm:
                        new = User(username=username, email=email, password=password)
                        new.save()
                        messages.success(request, "Account Created Successfully!")
                    else:
                        messages.error(request, "Passwords Don't match!")
                else:
                    messages.error(request, "Invalid password!")
                    messages.info(request, "Passwords should contain any of the four character types:   uppercase letters: (A-Z), lowercase letters: (a-z), numbers (0-9), and symbols (~`! @#$%^&*()_-+={[}]|\:;\"'<,>.?/)")
            else:
                messages.error(request, "Invalid Email!")
                messages.info(request,"Acceptable email prefix formats: Allowed characters: letters (a-z), numbers, underscores, periods, and dashes. Acceptable email domain formats Allowed characters: letters, numbers, dashes. The last portion of the domain must be at least two characters, for example: .com, .org, .cc")
        return redirect("/signup")
    else:
        form = AddUser()
    return render(request, 'marketplace/register.html', {'form':form})


def logout(request):
    auth_logout(request)
    return redirect("/")

@csrf_exempt
def search(request, query, category, filterBy, minPrice, maxPrice):
    class iTem:
        def __init__(self, title, price, image, category, description):
            self.title = title
            self.price = price
            self.image = image
            self.category = category
            self.description = description
    imAge = "https://static.wikia.nocookie.net/harrypotter/images/5/59/Elder_Wand.png/revision/latest?cb=20241227040818"
    data = {
        'items': [iTem("The Elder Wand", 2000000, imAge, "Magic", "The strongest wand ever"),
                  iTem("The Elder Wand", 2000000, imAge, "Magic", "The strongest wand ever"),
                  iTem("The Elder Wand", 2000000, imAge, "Magic", "The strongest wand ever"),
                  iTem("The Elder Wand", 2000000, imAge, "Magic", "The strongest wand ever"),]
    }
    return JsonResponse(data, safe=False)


@csrf_exempt
def upload(request):
    if request.method == "POST":
        print(request.FILES)
        response = "File uploaded successfully"
    else:
        response = f"Request method: {request.method}"
    return JsonResponse(response, safe=False)