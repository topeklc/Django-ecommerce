from curses.ascii import SI
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from payments import get_payment_model, RedirectNeeded

from .forms import PaymentForm, SignUpForm


def index(request):
    content = {}
    return render(request, "index.html", content)


def login(request):
    context = {}
    return render(request, "login.html", context)


def signup(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            print("valid!")
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.first_name = user.first_name.title()
            user.first_name = user.first_name.title()
            user.save()
            # login()

    context = {"signup_form": form}
    return render(request, "signup.html", context)


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
