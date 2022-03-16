from logging import PlaceHolder
from django import forms
from django.contrib.auth.models import User
from payments import get_payment_model
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
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

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )


class PaymentForm(forms.ModelForm):
    class Meta:
        model = get_payment_model()
        fields = ["variant", "total"]
