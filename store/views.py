from curses.ascii import SI
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from flask_login import login_required
from payments import get_payment_model, RedirectNeeded
from .models import User, Product
from .forms import LoginForm, PaymentForm, SignUpForm, AddressForm


def index(request):
    content = {}
    return render(request, "index.html", content)


def login_user(request):
    form = LoginForm()
    if request.user.is_authenticated:
        redirect("index")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist.")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Wrong password.")

    context = {"form": form}
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    messages.info(request, "User was logged out!")
    return redirect("login")


def signup(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.first_name = user.first_name.title()
            user.last_name = user.last_name.title()
            user.save()
            messages.success(request, "User account was created!")
            login(request, username=user.username, password=user.password)
        else:
            print(form.error_messages)
            messages.error(request, "An error has occured during registration: ")

    context = {"form": form}
    return render(request, "signup.html", context)


# @login_required
def user_address(request):
    form = AddressForm()
    if request.method == "POST":
        form = AddressForm(request.POST)
        user = request.user
        if form.is_valid():
            form = form.save(commit=False)
            form.user = user
            form.save()
            return redirect("index")
    context = {"form": form}

    return render(request, "address.html", context)


def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)
    try:
        form = payment.get_form(data=request.POST)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    return TemplateResponse(request, "payment.html", {"form": form, "payment": payment})


def create_payment(request):
    form = PaymentForm()
    if request.method == "POST":
        p = form.instance
        p.save()
        return redirect(f"payment-details/{p.id}")
    content = {"form": form}
    return render(request, "payments.html", content)


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    images = product.images.all()
    images = ["/".join(str(image.image).split("/")[1:]) for image in images]
    context = {"product": product, "images": images}

    return render(request, "product-detail.html", context)
