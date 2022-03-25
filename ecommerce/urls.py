"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from store import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("payments/", views.create_payment),
    path("payments/payment-details/<int:payment_id>", views.payment_details),
    path("login/", views.login_user, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout_user, name="logout"),
    path("address/", views.user_address, name="address"),
    path("product/<str:pk>/", views.product_detail, name="product-detail"),
    path("checkout/", views.checkout, name="checkout"),
]
