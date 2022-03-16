from django.contrib import admin
from store.models import *

# Register your models here
admin.site.register(Address)
admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Payment)
