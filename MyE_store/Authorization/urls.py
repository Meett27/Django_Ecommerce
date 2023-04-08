from django.urls import path, include
from Authorization.views import *

app_name= 'authorization'

urlpatterns = [
    path('signUp_page/', SignUpView.as_view(),name='signup_page'),
    path('', AuthenticationView.as_view(),name='login_page'),
]