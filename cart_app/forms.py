from django import forms
from .models import ShippingAddress,User
from django.contrib.auth.models import User





class AddressForm(forms.ModelForm):

	class Meta:

		model = ShippingAddress
		fields = ["name","address","city","state","zipcode"]