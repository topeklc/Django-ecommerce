from django.contrib import admin
from store.models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]


# Register your models here
admin.site.register(Address)

admin.site.register(Product, ProductAdmin)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Payment)
