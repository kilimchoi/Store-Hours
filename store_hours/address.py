from django.forms import ModelForm 
from django.db import models

class Address(models.Model):
	address1 = models.CharField()
	address2 = models.CharField()
	city = models.CharField()
	zip_code = models.IntegerField()

class AddressForm(ModelForm):
	class Meta: 
		model = Address