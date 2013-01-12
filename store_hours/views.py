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


def stores_branches(request):	
	if request.method == "POST":
		if 'address1' in request.POST and 'address2' in request.POST and 'city' in request.POST and 'zip_code' in request.POST:
			address1 = request.POST['address1']
			address2 = request.POST['address2']
			city = request.POST['city']
			zip_code = request.POST['zip_code']
			add = address1 + " " + address2 + " " + city + " " + zip_code
			add = urllib2.quote(add)
			geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % add
			req = urllib2.urlopen(geocode_url)
			address_json = json.loads(req.read())	
			if address_json['status'] == 'OK':
				latitude = address_json['results'][0]['geometry']['location']['lat']
				longitude = address_json['results'][0]['geometry']['location']['lng']
			nearby_store_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%f,%f&keyword=SAFEWAY|walgreens|Andronicos|WholeFoodsMarket&rankby=distance&types=store&sensor=false&key=AIzaSyABL0H4Lpi2HeiWFTzqC_xXpN7cH4bt2AA" % (latitude, longitude)
			store_req = urllib2.urlopen(nearby_store_url)
			store_json = json.loads(store_req.read())
			stores = []
			banks = []
			for store in store_json['results']:
				if store['name'] == u'SAFEWAY' or store['name'] == u'Walgreens' or store['name'] == u'Whole Foods Market' or store['name'] == u"Andronico's":
					stores.append(store)
			nearby_bank_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=37.874745,-122.264502&name=Wells|america|Chase&keyword=bank&rankby=distance&sensor=false&key=AIzaSyABL0H4Lpi2HeiWFTzqC_xXpN7cH4bt2AA"
			bank_req = urllib2.urlopen(nearby_bank_url)
			bank_json = json.loads(bank_req.read())
			
			for bank in bank_json['results']:
				if bank['name'] == u'Bank of America' or bank['name'] == u'Chase' or bank['name'] == u'Wells Fargo Bank':
					banks.append(bank)
			pprint.pprint(banks)
			#next_page_token = jsonResponse2['next_page_token']
			#next_page_token = next_page_token.encode('utf-8')
			#print "next_page_token is: ", next_page_token
			#nearby_search_url3 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=37.874745,-122.264502&radius=1000&types=store&hasNextPage=true&nextPage()=true&rankby=distance&sensor=false&key=AIzaSyABL0H4Lpi2HeiWFTzqC_xXpN7cH4bt2AA&pagetoken=%s" % next_page_token
			#req3 = urllib2.urlopen(nearby_search_url3)
			#jsonResponse3 = json.loads(req3.read())
			#pprint.pprint(jsonResponse3)
			#for jsonres in jsonResponse3['results']:
				#word = u'SUBWAY'
				#pprint.pprint(jsonres['name'])
			#geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true" % add
			#req = urllib2.urlopen(geocode_url)
			#jsonResponse = json.loads(req.read())
			open_boolean = True
			request.session['address1'] = address1
			request.session['address2'] = address2	
			request.session['city'] = city
			request.session['zip_code'] = zip_code
			if open_boolean:
				open_or_not = 'OPEN'
			else:
				open_or_not = 'CLOSED'
			dict = {'address1': address1, 'address2': address2, 'open_or_not': open_or_not, 'open_boolean': open_boolean}#'latitude': latitude, 'longitude': longitude}	
			template = "static/stores_branches.html"
			html = render_to_string(template, {'open_boolean': open_boolean, 'open_or_not': open_or_not})
			response = simplejson.dumps({'success': 'True', 'html': html})
			return render_to_response('static/stores_branches.html', dict, context_instance=RequestContext(request))
	return render_to_response('static/stores_branches.html', '', context_instance=RequestContext(request))

def specific_store_display(request):
	#next_page_token = jsonResponse2['next_page_token']
	#next_page_token = next_page_token.encode('utf-8')
	#print "next_page_token is: ", next_page_token
	#nearby_search_url3 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=37.874745,-122.264502&rankby=distance&types=store&hasNextPage=true&nextPage()=true&sensor=false&key=AIzaSyABL0H4Lpi2HeiWFTzqC_xXpN7cH4bt2AA&pagetoken=%s" % next_page_token
	#req3 = urllib2.urlopen(nearby_search_url3)
	#jsonResponse3 = json.loads(req3.read())
	#pprint.pprint(jsonResponse3)
	#for jsonres in jsonResponse3['results']:
		#pprint.pprint(jsonres['name'])
	return render_to_response('static/specific_store_display.html', '', context_instance=RequestContext(request))

