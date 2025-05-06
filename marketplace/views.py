from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LogUser, AddUser
from django.http import JsonResponse
from django.db.models import Count
from django.utils.timezone import now, timedelta
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
        product.name = request.POST["title"]
        product.price = request.POST["price"]
        if int(request.POST["stock"]) == 1:
            product.inStock = True
        else:
            product.inStock = False
        product.category = SubCategory.objects.get(title=request.POST["category"])
        product.description = request.POST["description"]
        product.specification = dict(zip(request.POST['spec_keys'].split(","), request.POST['spec_values'].split(",")))
        product.rating = request.POST['rating']
        product.tag = request.POST['tag']
        product.save()
        
    images = []
    for img in Item_image.objects.filter(item=Item.objects.get(pk=int(id))):
        images.append({"file": img.file.url,
                       "id": img.id})
    context = {
        "product": product,
        "categories": SubCategory.objects.all(),
        "images": images,
        "specification": product.specification,
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
        product.description = request.POST["description"]
        specification = dict(zip(request.POST['spec_keys'], request.POST['spec_values']))
            
        Item.objects.create(name=title, price=price, inStock=inStock, category=category, specification=specification)
        return JsonResponse(Item.objects.get(name=title, price=price, inStock=inStock, category=category).id, safe=False)
    context = {
        "categories": SubCategory.objects.all(),
    }
    return render(request, 'marketplace/add_product.html', context)

def stats(request):
    total_requests = Order.objects.count()

    # Requests per status
    status_counts = Order.objects.values('status').annotate(count=Count('status'))

    # Requests over last 7 days
    last_7_days = [now().date() - timedelta(days=i) for i in range(6, -1, -1)]
    daily_counts = []
    for day in last_7_days:
        count = Order.objects.filter(created_at__date=day).count()
        daily_counts.append({'date': day.strftime('%Y-%m-%d'), 'count': count})

    # Requests per user
    user_counts = Order.objects.values('user__username').annotate(count=Count('id')).order_by('-count')[:5]

    # Recent requests
    recent_requests = Order.objects.select_related('user').order_by('-created_at')[:10]

    return render(request, 'marketplace/stats.html', {
        'total_requests': total_requests,
        'status_counts': status_counts,
        'daily_counts': daily_counts,
        'user_counts': user_counts,
        'recent_requests': recent_requests
    })

def media(request):
    request_files = []
    item_images = []
    for file in RequestFile.objects.all():
        request_files.append(file)
    for file in Item_image.objects.all():
        item_images.append(file)
    context = {
        "media_files": {
            "request_files": request_files,
            "item_images": item_images
        }
    }
    return render(request, 'marketplace/media.html', context)

def users(request):
    all_users = []
    for usr in User.objects.filter(is_staff=False):
        temp = UserProfile.objects.get(user=usr)
        all_users.append({"username": usr.username, "image": temp.image, "email": usr.email, "full_name": temp.full_name, "phone": temp.phone_number})
    print(all_users)
    context = {
        'users': all_users,
    }
    return render(request, 'marketplace/users.html', context)
    
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
    if request.POST:
        Review.objects.create(user=request.user, item=product, rating=request.POST['rating'], comment=request.POST['content'])
 
    context = {
        "product": {
            "id": product.id,
            "title": product.name,
            "description": product.description,
            "price": product.price,
            "inStock": product.inStock,
            "stock_range": range(1, 6),
            "specification": product.specification,
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
    