from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LogUser, AddUser
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .models import UserProfile, Category, SubCategory, Item, Item_image, Order, Request, RequestFile, Review
import re
import json



# Main Page
def main(request):
    categories = [{"category": category.title, "image": category.image.url, "subs": [sub.title for sub in SubCategory.objects.filter(parent=category)]} for category in Category.objects.all()]
    items = [{"title": product.name, "category": product.category.title, "price": product.price, "rating": range(5), "description": str(product.description)[:50] + "..","image": list(Item_image.objects.filter(item=product))[0].file.url} for product in Item.objects.all()]
    context = {"items": items,
                "categories": categories
                }
    return render(request, 'marketplace/index.html', context)

# Store Page
def store(request):
    context = {
        "categories": [
            {"title": category.title, "subs": [sub.title for sub in SubCategory.objects.filter(parent=category)]} for category in Category.objects.all()
        ]
    }
    return render(request, 'marketplace/store.html', context)

    
# Admin Page
def admin(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        otp = request.POST['otp']
        # Authentication
        try:
            user = User.objects.get(username=username, is_superuser=True)
            if user.password != password:
                messages.error(request,'Invalid password')
                return redirect("hq")
        except User.DoesNotExist:
            user = None
        # If authentication is successful Login
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"{username} Logged In Successfully!")
            return redirect("hq-r")
        else:
            messages.error(request, "Cannot Log In!")
            return redirect("hq")
    return render(request, 'marketplace/admin.html')
    
def requests(request):
    requests = Request.objects.all().order_by('-date_created')
    return render(request, 'marketplace/requests.html', {'requests': requests})

@csrf_exempt
@require_POST
def update_order_status(request):
    data = json.loads(request.body)

    try:
        ord = Order.objects.get(pk=data['id'])
        if data['status'] in ['approved', 'declined']:
            ord.status = data['status']
            ord.save()
            return JsonResponse({'success': True, 'new_status': ord.get_status_display()})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid status'})
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Order not found'})
        
@csrf_exempt
@require_POST
def update_request_status(request):
    data = json.loads(request.body)

    try:
        req = Request.objects.get(pk=data['id'])
        if data['status'] in ['approved', 'declined']:
            req.status = data['status']
            req.save()
            return JsonResponse({'success': True, 'new_status': req.get_status_display()})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid status'})
    except Request.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Request not found'})

def orders(request):
    context = {'orders': Order.objects.all()
              }
    return render(request, 'marketplace/orders.html', context)

def view_products(request):
    context = {'products': [
                            {"id": item.id,
                             "name": item.name,
                             "price": item.price,
                             "created_at": item.created_at,
                             "inStock": item.inStock,
                             "category": item.category,
                             "image": list(Item_image.objects.filter(item=item))[0]} for item in Item.objects.all()]}    
    return render(request, 'marketplace/products.html', context)

@csrf_exempt
def get_product_images(request, id):
    images = []
    for img in Item_image.objects.filter(item=Item.objects.get(pk=int(id))):
        images.append({"file": img.file.url,
                       "id": img.id})
    data = {"images": images}
    return JsonResponse(data, safe=False)
    
@csrf_exempt
def remove_product_img(request):
    if request.POST:
        Item_image.objects.get(pk=request.POST['id']).delete()
        data = f"Item deleted {request.POST['id']}"
    else:
        data = "No request have been made"
    return JsonResponse(data, safe=False)
 
@csrf_exempt
def edit_product(request, id):
    product = Item.objects.get(pk=id)
    if request.method == "POST":
        product.title = request.POST["title"]
        product.price = request.POST["price"]
        if int(request.POST["stock"]) == 1:
            product.inStock = True
        else:
            product.inStock = False
        product.category = SubCategory.objects.get(title=request.POST["category"])
        product.save()
        
    images = []
    for img in Item_image.objects.filter(item=Item.objects.get(pk=int(id))):
        images.append({"file": img.file.url,
                       "id": img.id})
    context = {
        "product": product,
        "categories": SubCategory.objects.all(),
        "images": images,
    }
    return render(request, 'marketplace/edit_product.html', context)
@csrf_exempt
def add_product(request):
    if request.POST:
        title = request.POST["title"]
        price = request.POST["price"]
        if int(request.POST["stock"]) == 1:
            inStock = True
        else:
            inStock = False
        category = SubCategory.objects.get(title=request.POST["category"])
        Item.objects.create(name=title, price=price, inStock=inStock, category=category) # TO DO
        return JsonResponse(id, safe=False)
    context = {
        "categories": SubCategory.objects.all(),
    }
    return render(request, 'marketplace/add_product.html', context)

def stats(request):    
    return render(request, 'marketplace/stats.html')

def media(request):
    context = {
        "media_files": [file for file in RequestFile.objects.all()]
    }
    return render(request, 'marketplace/media.html', context)

def users(request):
    all_users = [usr for usr in User.objects.filter()]
    context = {
        'users': all_users,
        'user_profiles': [profile for profile in UserProfile.objects.all() for usr in all_users if profile.user in all_users]
    }
    return render(request, 'marketplace/users.html')
    
def settings(request):
    context = {
        "user": request.user,
    }
    return render(request, 'marketplace/settings.html')

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
    if page == "logo":
        if request.POST:
            print(request.POST)
            return render(request, "marketplace/logo.html", context)
        else:
            return render(request, "marketplace/logo.html", context)

# Services
def services(request):
    return
    
# Single
def single(request, id):
    product = Item.objects.get(id=id)
    context = {
        "product": {
            "title": product.name,
            "description": product.description,
            "price": product.price,
            "inStock": product.inStock,
            "stock_range": range(1, 6),
            "specification": "",
            "reviews": list(Review.objects.filter(item=product)),
            "images": list(Item_image.objects.filter(item=product)),
        }
        
    }
    return render(request, "marketplace/single.html", context)

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
                    return redirect("login")
            except User.DoesNotExist:
                user = None
            # If authentication is successful Login
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"{username} Logged In Successfully!")
                return redirect("store")
            else:
                messages.error(request, "Cannot Log In!")
                return redirect("login")
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
        return redirect("signup")
    else:
        form = AddUser()
    return render(request, 'marketplace/register.html', {'form':form})


def logout(request):
    auth_logout(request)
    return redirect("/")

@csrf_exempt
def products(request):    
    data = {
        "items": [{"id": product.id,
                   "title": product.name,
                   "category": product.category.title,
                   "description": product.description,
                   "rating": 5,
                   "inStock": "1",
                   "price": product.price,
                   "tag": "New",
                   "image": [img.file.url for img in Item_image.objects.filter(item=product)]} for product in Item.objects.all()]
    }
    return JsonResponse(data, safe=False)


@csrf_exempt
def get_categories(request):
    data = {
        "categories": [
            {"title": category.title, "subs": [sub.title for sub in SubCategory.objects.filter(parent=category)]} for category in Category.objects.all()
        ]
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

@csrf_exempt
def update_product_img(request, id):
    product = Item.objects.get(pk=id)
    image = Item_image.objects.create(abbr=str(request.FILES.getlist('file')[0]), item=product, file=request.FILES.getlist('file')[0])
    image.save()
    response = "Image Uploaded Successfully"
    return JsonResponse(response, safe=False)
    