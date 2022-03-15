# Generated by Django 4.0.3 on 2022-03-15 21:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields
import store.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('number', models.PositiveIntegerField()),
                ('zip_code', models.CharField(max_length=10)),
                ('country', django_countries.fields.CountryField(countries=store.models.AvailableCountries, max_length=2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('discount', models.IntegerField(blank=True, null=True)),
                ('category', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=50)),
                ('brand_name', models.CharField(max_length=50)),
                ('url', models.SlugField()),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to=store.models.get_image_path)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.ImageField(default=1, upload_to='')),
                ('order_sum', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_sum', models.FloatField()),
                ('order_date', models.DateField(auto_now_add=True)),
                ('ordered', models.BooleanField(default=False)),
                ('shipped', models.BooleanField(default=False)),
                ('received', models.BooleanField(default=False)),
                ('refund', models.BooleanField(default=False)),
                ('refund_received', models.BooleanField(default=False)),
                ('products', models.ManyToManyField(to='store.orderproduct')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]