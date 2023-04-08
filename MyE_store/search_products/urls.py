from django.urls import path, include
from . import views

app_name= 'search_products'

urlpatterns = [
    path('', views.SearchProducts.as_view(), name='query'),
  
]