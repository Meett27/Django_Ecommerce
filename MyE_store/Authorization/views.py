from django.http import request, JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect  
from django.views.decorators.cache import never_cache 
from .forms import * 
from django.urls import reverse_lazy
# Create your views here.



class AuthenticationView(FormView):
    Model = User
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('store:home')
    

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(AuthenticationView, self).dispatch(*args, **kwargs)  

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        can log him in.
        """
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)      
    


class SignUpView(FormView):
    Model = User
    template_name = 'signupForm.html'
    signUp_form_class = SignUpForm
    success_url = reverse_lazy('authorization:login_page')

    def get(self, request,*args,**kwargs):
        signUp_form = self.signUp_form_class()    
        return render(request, self.template_name, {'signUp_form':signUp_form})
    
    def post(self,request,*args,**kwargs):
        signUp_form = self.signUp_form_class(self.request.POST)  

        if signUp_form.is_valid():
            username = self.request.POST.get('username')
            first_name = self.request.POST.get('first_name')
            last_name = self.request.POST.get('last_name')
            email = self.request.POST.get('email')
            password = self.request.POST.get('password2')
            User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
            return HttpResponseRedirect(self.success_url)
        else :
            return redirect('authorization:signup_page')   

    

