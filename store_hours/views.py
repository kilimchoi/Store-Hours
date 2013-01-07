from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from address import Address, AddressForm
from django.template.loader import render_to_string
import urllib2
import pprint
import json

def index(request):
    return render_to_response('static/index.html', '', context_instance=RequestContext(request))


def store_display(request):	
	if request.method == "POST":
		if 'address1' in request.POST and 'address2' in request.POST and 'city' in request.POST and 'zip_code' in request.POST:
			address1 = request.POST['address1']
			address2 = request.POST['address2']
			store_branch = request.POST['store_branch']
			city = request.POST['city']
			zip_code = request.POST['zip_code']
			add = address1 + " " + address2 + " " + city + " " + zip_code
			add = urllib2.quote(add)
			geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true" % add
			print geocode_url
			req = urllib2.urlopen(geocode_url)
			jsonResponse = json.loads(req.read())
			if jsonResponse['status'] == 'OK':
				latitude = jsonResponse['results'][0]['geometry']['location']['lat']
				longitude = jsonResponse['results'][0]['geometry']['location']['lng']
			open_boolean = True
			request.session['address1'] = address1
			request.session['address2'] = address2
			request.session['store_branch'] = store_branch
			request.session['city'] = city
			request.session['zip_code'] = zip_code
			if open_boolean:
				open_or_not = 'OPEN'
			else:
				open_or_not = 'CLOSED'
			dict = {'address1': address1, 'address2': address2, 'store_branch': store_branch, 'open_or_not': open_or_not, 'open_boolean': open_boolean, 'latitude': latitude, 'longitude': longitude}			
			template = "static/specific_store_display.html"
			html = render_to_string(template, {'store_branch': store_branch, 'open_boolean': open_boolean, 'open_or_not': open_or_not})
			response = simplejson.dumps({'success': 'True', 'html': html})
			return render_to_response('static/specific_store_display.html', dict, context_instance=RequestContext(request))
	return render_to_response('static/specific_store_display.html', '', context_instance=RequestContext(request))

def branches_display(request):
	return render_to_response('static/stores_branches.html', '', context_instance=RequestContext(request))

