from django.db import models
from django.conf import settings
from django.db.models import Q
from django.db.models.deletion import CASCADE
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save

# Create your models here.



# Category
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    image=models.ImageField(upload_to="cat_imgs/",null=True, blank=True)
    def __str__(self):
        return self.category_name

    # def get_absolute_url(self):
    #     return reverse("store:product_by_category", kwargs={
    #     'cat_id': self.cat_id
    #    })

# Brand
class Brand(models.Model):
    title=models.CharField(max_length=100,  unique=True)

    def __str__(self):
        return self.title



class ProductQueryset(models.QuerySet):
    def featured (self):
        return self.filter(featured=True)   
                                                                          
    def search(self, query):
        lookups = (  
                Q(title__icontains=query) |
                Q(price__icontains=query)|
                Q(details__icontains=query)|
                Q(brand__title__icontains=query)|
                Q(subcategory__icontains=query)|
                Q(category__category_name__icontains=query)
            )
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):

    def get_by_id(self, slug):
        qs = self.get_queryset().filter(slug=self.slug)
        if qs.count == 1:
            return qs.first()
        return None

    def get_queryset(self):
        return ProductQueryset(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


class Item(models.Model):
    title = models.CharField(max_length=100)
    details = models.CharField(max_length=1000)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=100, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=False, blank=False)
    price = models.FloatField(null=False,blank=False)
    slug = models.SlugField( blank=True, unique=True)
    image = models.ImageField(upload_to="prod_imgs/",null=True, blank=True)

    objects = ProductManager()

    def __str__(self) :
        return self.title

    def get_absolute_url(self):
        return reverse("store:item", kwargs={
        'slug': self.slug
       })

def item_pre_save_recevier(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(item_pre_save_recevier, sender=Item)


# Shipping Address
class ShippingAddress(models.Model):
    id = models.AutoField(primary_key=True)
    address_line1 = models.CharField(max_length=200, null=False)
    address_line2 = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.address_line1



# Customer profile
class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15,null=True, blank=True)
    address = models.ManyToManyField(ShippingAddress,blank=True)
    def __str__(self):
        return self.user.name

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=240, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_subtotal(self):
        orderitems = self.orderitem_set.all()
        subtotal = sum([item.get_subtotal for item in orderitems])
        return subtotal

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item for item in orderitems])
        return total


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    @property
    def get_subtotal(self):
        total = self.product.price * self.quantity
        subtotal = total + (total * 0.18)
        return subtotal