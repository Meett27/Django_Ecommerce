
from django.http import request, JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import *
from .models import *
import json
from .forms import * 
from django.urls import reverse_lazy
# Create your views here.

class Home(TemplateView):
    template_name = 'index.html'
    model = Item, Category

    def get_context_data(self, *args, **kwargs):
        ctx = super(Home, self).get_context_data(*args, **kwargs)
        ctx["items"]=Item.objects.filter(quantity__gte=10).order_by('id')[:20]
        ctx["category"] = Category.objects.all()
        if self.request.user.is_authenticated:
            customer = self.request.user.profile
            order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        
        items = order.orderitem_set.all()
        cart_items = 0
        for i in items:
            cart_items +=1

        ctx["cartItems"] = cart_items
        return ctx
    
   

class ProductDetails(TemplateView):
    query_set = Item.objects.all()
    template_name = 'details.html'
    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug')
        context = super(ProductDetails, self).get_context_data(**kwargs)
        context['object'] = Item.objects.get(slug=slug)
        item = Item.objects.get(slug=slug)
        if self.request.user.is_authenticated:
            customer = self.request.user.profile
            order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = 0
        for i in items:
            cart_items +=1

        context["cartItems"] = cart_items
        context['related_products'] = Item.objects.filter().exclude(slug=slug)
       
        return context

class Product_categories(ListView):
    queryset = Item.objects.all()
    template_name = 'category.html'


    def get_context_data(self, *args, **kwargs): 
        context = super(Product_categories, self).get_context_data(*args, **kwargs)
        first_category = Category.objects.all()[0]
        context["items"]=Item.objects.filter(category=first_category)
        context["categories"] = Category.objects.all()
        category_list = list(Category.objects.all())
        counts = {}
        for i in category_list:
            filter_items = list(Item.objects.filter(category=i).order_by('id'))
            print(filter_items)
            counts[i.category_name] = len(filter_items)
        context["counts"] = counts  

        if self.request.user.is_authenticated:
            customer = self.request.user.profile
            order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = 0
        for i in items:
            cart_items +=1

        context["cartItems"] = cart_items

        return context
            


class Products_by_categories(ListView):
    queryset = Item.objects.all()
    template_name = 'category.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        cat_id = self.kwargs.get('cat_id')
        product_category = Category.objects.get(id=cat_id)
        context["products_by_cat"]=Item.objects.filter(category=product_category).order_by('id')
        context["categories"] = Category.objects.all()
        category_list = list(Category.objects.all())
        counts = {}
        for i in category_list:
            filter_items = list(Item.objects.filter(category=i).order_by('id'))
            print(filter_items)
            counts[i.category_name] = len(filter_items)
        context["counts"] = counts

        if self.request.user.is_authenticated:
            customer = self.request.user.profile
            order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = 0
        for i in items:
            cart_items +=1
        
        context["cartItems"] = cart_items
        
        
        return context
        
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = 0
        for i in items:
            cart_items +=1

        cartItems = cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = Order.get_cart_items
        
    context = {'items': items, 'order': order, 'cartItems':cartItems}
    return render(request, 'cart.html', context)   

def update_cart_items(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print("Action:", action)
    print("ProductId:", productId)

    customer = request.user.profile
    product = Item.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    oderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == "added":
        oderItem.quantity = (oderItem.quantity + 1)
    elif action == "remove":
        oderItem.quantity = (oderItem.quantity - 1)

    oderItem.save()

    if oderItem.quantity <= 0:
        oderItem.delete()
    
    if action == "delete":
        oderItem.delete()
    return JsonResponse("Item was added", safe=False)
    
class ProfileDetails(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            customer = self.request.user
        context["profile"] = Profile.objects.get(user=customer)
      
        return context

class UpdateUserProfile(FormView):
        Model = User,Profile,ShippingAddress
        user_form_class = UpdateUserProfile
        profile_form_class = EditUserProfileForm
        
        template_name = 'edit_profile.html'  
        success_url = reverse_lazy('store:profile')
    

        def get(self, request,*args,**kwargs):
            if request.user.is_authenticated:
                customer = request.user
                profile_object = Profile.objects.get(user=customer)
            user_form = self.user_form_class(instance=customer)
            profile_form = self.profile_form_class(instance=profile_object)
            return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})


        def post(self,request,*args,**kwargs):
            if request.user.is_authenticated:
                customer = request.user
                profile_object = Profile.objects.get(user=customer)
            user_form = self.user_form_class(self.request.POST,instance=customer)
            profile_form = self.profile_form_class(self.request.POST,instance=profile_object)
           

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return HttpResponseRedirect(self.success_url)
            else :
                return self.form_invalid(user_form,profile_form,**kwargs)

        def form_invalid(self, user_form,profile_form):
            user_form = self.user_form_class()
            profile_form = self.profile_form_class()
            return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})
            