from django.http import request
from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView
from store.models import *

# Create your views here.
class SearchProducts(ListView):
    template_name = 'search_view.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        
        if query is not None:
            return Item.objects.search(query)
        return "Not Found"
    
