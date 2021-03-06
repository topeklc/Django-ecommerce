from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User
from payments import get_payment_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Address, Order, ProductReview, OrderProduct


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("User with that email already exists")
        return email

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password1"]

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )


class PaymentForm(forms.ModelForm):
    class Meta:
        model = get_payment_model()
        fields = ["variant", "total"]


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ["user", "first_name", "last_name", "email"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ["review_text", "rating"]


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ["quantity"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
