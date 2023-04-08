from django.contrib import admin
from .models import *
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','title','slug','category','brand','subcategory','details','quantity','price')
    class Meta:
        model = Item

# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('id','user','name','email','mobile_no')
#     class Meta:
#         model = Profile

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id','address_line1','address_line2','city','state','zipcode','country')
    class Meta:
        model = ShippingAddress

admin.site.register(Item,ProductAdmin )
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ShippingAddress,ShippingAddressAdmin)
admin.site.register(Profile)