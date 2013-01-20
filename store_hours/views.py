from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from datetime import datetime
import urllib2
import pprint
import json

def index(request):
	return render_to_response('static/index.html', '', context_instance=RequestContext(request))

def hours_display(request, store_branch_name, address):
	time = ""
	mon_fri_time = ""
	sat_time = ""
	sun_time = ""
	open_boolean = False
	if_bank = False
	temp_add = address
	address = address.replace(" ", "")
	open_or_not = ""
	if store_branch_name == "Safeway":
		time = "6 am - 12 am"
		if "5130Broadway" in address:
			time = "24 hours"
		if "6310 College" in address:
			time = "24 hours"
	if store_branch_name == "Whole Foods Market" or store_branch_name == "Whole foods Market" :
		time = "8 am - 10 pm"
	if store_branch_name == "Andronico's":
		if "1850Solano" in address:
			time = "8 am - 9 pm"
		if "1550Shattuck" in address:
			time = "8 am - 10 pm"
	if store_branch_name == "Bank of America":
		if_bank = True
		mon_fri_time = "9 am - 6 pm" 
		sat_time = "9 am - 2 pm"
		sun_time = "CLOSED"
	if store_branch_name == "Chase Bank":
		if_bank = True
		mon_fri_time = "9 am - 6 pm" 
		sat_time = "9 am - 4 pm"
		sun_time = "CLOSED"
	if store_branch_name == "Wells Fargo Bank":
		if_bank = True
		mon_fri_time = "9 am - 6 pm" 
		sat_time = "9 am - 6 pm"
		sun_time = "CLOSED"
	time_list = [int(t) for t in time.split() if t.isdigit()]
	weekday = datetime.today().weekday()
	mon_fri_list = [int(t) for t in mon_fri_time.split() if t.isdigit()]
	sat_list = [int(t) for t in sat_time.split() if t.isdigit()]
	now = datetime.now()
	hour = now.hour
	if time_list and hour >= time_list[0] and hour <= time_list[1] + 12:
		open_boolean = True
	if mon_fri_list and hour >= mon_fri_list[0] and hour <= mon_fri_list[1] + 12:
		if weekday <= 4 and weekday >= 0:
			open_boolean = True
	if sat_list and hour >= sat_list[0] and hour <= sat_list[1] + 12:
		if weekday == 5:
			open_boolean = True
	if open_boolean:
		open_or_not = "OPEN"
	else:
		open_or_not = "CLOSED"
	temp_add = urllib2.quote(temp_add)
	geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % temp_add
	req = urllib2.urlopen(geocode_url)
	address_json = json.loads(req.read())
	if address_json['status'] == 'OK':
		latitude = address_json['results'][0]['geometry']['location']['lat']
		longitude = address_json['results'][0]['geometry']['location']['lng']
	dict = {"time": time, "mon_fri_time": mon_fri_time, "sat_time": sat_time, "sun_time": sun_time, "open_boolean": open_boolean, "store_branch": store_branch_name, "open_or_not": open_or_not, "if_bank": if_bank, 'latitude': latitude, 'longitude': longitude}
	return render_to_response('static/hours_display.html', dict, context_instance=RequestContext(request))

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
				if store['name'] == u'SAFEWAY' or store['name'] == u'Whole Foods Market' or store['name'] == u"Andronico's":
					stores.append(store)
			stores = choose_best(stores)
			new_stores = []
			new_stores = stores.values()
			nearby_bank_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=37.874745,-122.264502&name=Wells|america|Chase&keyword=bank&rankby=distance&sensor=false&key=AIzaSyABL0H4Lpi2HeiWFTzqC_xXpN7cH4bt2AA"
			bank_req = urllib2.urlopen(nearby_bank_url)
			bank_json = json.loads(bank_req.read())
			for bank in bank_json['results']:
				if bank['name'] == u'Bank of America' or bank['name'] == u'Chase' or bank['name'] == u'Wells Fargo Bank':
					banks.append(bank)
			banks = choose_best(banks)
			new_banks = []
			new_banks = banks.values()
			dict = {'address1': address1, 'address2': address2, 'stores': new_stores, 'banks': new_banks}		
			return render_to_response('static/stores_branches.html', dict, context_instance=RequestContext(request))
	
def choose_best(stores):
	max_rating_stores = {}
	first_time = False
	prev = ""
	curr = ""
	temp_stores = stores
	stores = [store for store in stores if 'rating' in store]
	reversed(sorted(stores, key=lambda store:store['rating']))
	if len(stores) <= 3:
		stores = temp_stores
	for store in stores:
		if 'opening_hours' in store:
			curr = store
			if first_time:
				if store['name'] not in max_rating_stores:
					max_rating_stores[store['name']] = store
			else:
				first_time = True
				prev = curr
				max_rating_stores[store['name']] = store
        prev = curr
	return max_rating_stores

def branches_display(request):
	if request.method == "POST":
		if 'address1' in request.POST and 'address2' in request.POST and 'city' in request.POST and 'zip_code' in request.POST:
			address1 = request.POST['address1']
			address2 = request.POST['address2']
			city = request.POST['city']
			zip_code = request.POST['zip_code']
			store_branch = request.POST['store_branch']
			permanent_store_branch = store_branch
			bank_boolean = False
			stores = []
			new_stores = []
			banks = []
			new_banks = []
			if "bank" in store_branch or "Bank" in store_branch:
				bank_boolean = True
			add = address1 + " " + address2 + " " + city + " " + zip_code
			add = urllib2.quote(add)
			geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % add
			req = urllib2.urlopen(geocode_url)
			address_json = json.loads(req.read())	
			if address_json['status'] == 'OK':
				latitude = address_json['results'][0]['geometry']['location']['lat']
				longitude = address_json['results'][0]['geometry']['location']['lng']
			if not bank_boolean:
				store_branch = choose_store_branch(store_branch)
				nearby_branch_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%f,%f&keyword=%s&rankby=distance&types=store&sensor=false&key=AIzaSyABL0H4Lpi2HeiWFTzqC_xXpN7cH4bt2AA" % (latitude, longitude, store_branch)
				store_req = urllib2.urlopen(nearby_branch_url)
				store_json = json.loads(store_req.read())
				for store in store_json['results']:
					name = store['name'].encode('utf-8')
					name = name.lower()
					name = name.replace("'", "")
					name = name.replace(" ", "")
					store_branch = store_branch.lower()
					if name == store_branch:
						stores.append(store)
				stores = choose_best_five(stores)
				new_stores = stores
			else:
				store_branch = choose_bank_branch(store_branch)
				nearby_bank_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=37.874745,-122.264502&name=%s&keyword=bank&rankby=distance&sensor=false&key=AIzaSyABL0H4Lpi2HeiWFTzqC_xXpN7cH4bt2AA" % store_branch
				bank_req = urllib2.urlopen(nearby_bank_url)
				bank_json = json.loads(bank_req.read())
				for bank in bank_json['results']:
					if bank['name'] == u'Bank of America' or bank['name'] == u'Chase' or bank['name'] == u'Wells Fargo Bank':
						banks.append(bank)
				banks = choose_best_five(banks)
				new_banks = banks
			dict = {'address1': address1, 'address2': address2, 'stores': new_stores, 'banks': new_banks, 'store_branch': permanent_store_branch}		
			return render_to_response('static/branches_display.html', dict, context_instance=RequestContext(request))

def choose_best_five(stores):
	max_rating_stores = []
	first_time = False
	temp_stores = stores
	counter = 0
	stores = [store for store in stores if 'rating' in store]
	reversed(sorted(stores, key=lambda store:store['rating']))
	if len(stores) <= 3:
		stores = temp_stores
	for store in stores:
		if 'opening_hours' in store:
			if counter == 5:
				break
			else:
				max_rating_stores.append(store)
				counter = counter + 1
	return max_rating_stores

def choose_store_branch(store_name):
	if store_name == "Whole Foods":
		store_name = "WholeFoodsMarket"
	if store_name == "Safeway":
		store_name = "SAFEWAY"
	if store_name == "Andronicos":
		store_name = "Andronicos"
	return store_name

def choose_bank_branch(bank_name):
	if bank_name == "Bank of America":
		bank_name = "america"
	if bank_name == "Chase Bank":
		bank_name = "Chase"
	if bank_name == "Wells Fargo Bank":
		bank_name = "Wells"
	return bank_name

