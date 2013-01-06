from django import forms

class AddressForm(forms.Form):
	address1 = forms.CharField()
	address2 = forms.charField()
	city = forms.charField()
	zip_code = forms.IntegerField()
	