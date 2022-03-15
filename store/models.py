from email.policy import default
import os
from django.db import models
from django.conf import settings
from django_countries.fields import CountryField, Countries
from phonenumber_field.modelfields import PhoneNumberField
from telegram import ShippingAddress


def get_image_path(instance, filename):
    return os.path.join("static", "photos", str(instance.brand_name), filename)


CATEGORIES_LIST = [("A", "A"), ("B", "B"), ("C", "C")]


class AvailableCountries(Countries):
    only = ["PL", ("EU", ("European Union"))]


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = PhoneNumberField()

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    zip_code = models.CharField(max_length=10)
    country = CountryField(countries=AvailableCountries)


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    discount = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORIES_LIST)
    brand_name = models.CharField(max_length=50)
    url = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to=get_image_path)

    def __str__(self):
        return self.name


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1)
    order_sum = order_sum = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.order_sum = (
            self.quantity * self.product.price * (1 - self.product.discount / 100)
        )
        super(OrderProduct, self).save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    order_sum = models.FloatField()
    order_date = models.DateField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, blank=True, null=True
    )
    # payment = models.ForeignKey(
    #     Payment, on_delete=models.SET_NULL, blank=True, null=True
    # )
    shipped = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund = models.BooleanField(default=False)
    refund_received = models.BooleanField(default=False)

    def get_total(self):
        total = 0
        for ordered_product in self.products.all():
            total += ordered_product.order_sum
        return total

    def save(self, *args, **kwargs):
        self.order_sum = self.get_total
        super(OrderProduct, self).save(*args, **kwargs)
