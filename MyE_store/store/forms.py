
from django import forms
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.forms import fields  
from store.models import *
# from betterforms.multiform import MultiModelForm


class UpdateUserProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name'
        )

class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('mobile_no','address')
        address = forms.ModelChoiceField(
            queryset=ShippingAddress.objects.all(),
            widget=forms.SelectMultiple
        )

class EditUserAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('address_line1','address_line2','city','state','zipcode','country')    

