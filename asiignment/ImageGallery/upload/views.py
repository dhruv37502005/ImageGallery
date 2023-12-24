from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout

# from .tokens import generate_token
from PIL import Image


# Create your views here.
# Home page
def index(request):
    return render(request, "index.html")


# signup page
def user_signup(request):
    if request.method == "POST":
        # retrive form data
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        # validation
        if User.objects.filter(username=username).exists():
            messages.error(
                request, "Username already exists! Please try a different username."
            )
            return redirect("signup")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("signup")
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")
        else:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email,
            )
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return redirect("home")
    else:
        form = UserCreationForm()
        return render(request, "signup.html", {"form": form})


# login page
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("upload")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


# logout page
def user_logout(request):
    logout(request)
    return redirect("login")


def home(request):
    return render(request, "index.html")


def user_upload(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form)
            form.save()
            return redirect("display")
    else:
        form = ImageForm()
    img = Images.objects.all()
    return render(request, "upload.html", {"img": img, "formup": form})


def display_images(request):
    # print(":::display_images called")
    images = Images.objects.all().order_by("date")
    # last_is_landscape = Image.open(Images.objects.all().last().photo.path)
    portrait_images = []
    landscape_images = []
    last_land = False
    for image in images:
        with Image.open(image.photo.path) as img:
            width, height = img.size
            if width > height:
                landscape_images.append(image)
                last_land = True
            else:
                portrait_images.append(image)
                last_land = False
    sorted = []
    extra_land = None
    landscape_images.reverse()
    portrait_images.reverse()
    if last_land:
        extra_land = landscape_images.pop(0)
    for img in range(len(landscape_images)):
        sorted.append(
            [
                landscape_images[img],
                portrait_images[img * 2],
                portrait_images[img * 2 + 1],
            ]
        )
    for i in range(len(landscape_images) * 2, len(portrait_images)):
        sorted.append([None, portrait_images[i], portrait_images[i - 1]])

    context = {
        "portrait_images": portrait_images,
        "landscape_images": landscape_images,
        "sorted": sorted,
        "extra_land": extra_land,
    }
    return render(request, "display.html", context)


def delete_image(request, pk):
    img = get_object_or_404(Images, pk=pk)
    img.delete()
    messages.success(request, "Image deleted successfully.")
    return redirect("upload")
