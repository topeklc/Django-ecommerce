from email.policy import default
import os
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField, Countries
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from payments.models import BasePayment
from payments import PurchasedItem
from decimal import Decimal


def get_image_path(instance, filename):
    return os.path.join("static", "photos", str(instance.product.brand_name), filename)


class AvailableCountries(Countries):
    only = ["PL", ("EU", ("European Union"))]


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=60, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    zip_code = models.CharField(max_length=10)
    country = CountryField(countries=AvailableCountries)
    is_shipping = models.BooleanField(default=False)
    is_billing = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Addresses"


class Category(models.Model):
    name = models.CharField(max_length=50)
    url = models.SlugField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    discount = models.IntegerField(blank=True, null=True)
    discounted_price = models.FloatField(default=price)
    category = models.ManyToManyField(Category)
    brand_name = models.CharField(max_length=50)
    url = models.SlugField()
    short_description = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    overall_rating = models.FloatField(default=1, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def get_overall_rating(self):
        reviews = ProductReview.objects.filter(product=self.id)
        print(reviews)
        ratings = [rating.rating for rating in reviews]
        print(ratings)
        print(sum(ratings) / len(ratings))
        return sum(ratings) / len(ratings)

    def save(self, *args, **kwargs):
        if self.discount > 0:
            self.discounted_price = self.price * (1 - self.discount / 100)
        else:
            self.discounted_price = self.price
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=get_image_path)


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = [["user", "product"]]


class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order_sum = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.order_sum = int(self.quantity) * self.product.discounted_price
        super(OrderProduct, self).save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    order_sum = models.FloatField(default=0, blank=True, null=True)
    order_date = models.DateField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, blank=True, null=True
    )
    shipped = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund = models.BooleanField(default=False)
    refund_received = models.BooleanField(default=False)

    def get_total(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        total = 0
        for ordered_product in self.products.all():
            total += ordered_product.order_sum
        return total

    def save(self, *args, **kwargs):
        self.order_sum = self.get_total(*args, **kwargs)
        super(Order, self).save(*args, **kwargs)


class Payment(BasePayment):
    def get_failure_url(self):
        return "http://example.com/failure/"

    def get_success_url(self):
        return "http://example.com/success/"

    def get_purchased_items(self):
        for ordered_product in Order.products.all():
            yield PurchasedItem(
                name=ordered_product.product.name,
                sku=ordered_product.product.brand_name,
                quantity=ordered_product.quantity,
                price=Decimal(ordered_product.product.price),
                currency="PLN",
            )
