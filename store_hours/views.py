from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
def index(request):
    return render_to_response('static/index.html', '', context_instance=RequestContext(request))

def store_display(request):
	if request.method == "GET":
		if 'address1' in request.GET and 'address2' in request.GET and 'city' in request.GET and 'zip_code' in request.GET:
			address1 = request.GET.get('address1')
			address2 = request.GET.get('address2')
			store_branch = request.GET.get('store_branch')
			open_boolean = True
			if open_boolean:
				open_or_not = 'OPEN'
			else:
				open_or_not = 'CLOSED'
			dict = {'address1': address1, 'address2': address2, 'store_branch': store_branch, 'open_or_not': open_or_not, 'open_boolean': open_boolean} 
			return render_to_response('static/specific_store_display.html', dict, context_instance=RequestContext(request))
	return render_to_response('static/specific_store_display.html', '', context_instance=RequestContext(request))

def branches_display(request):
	return render_to_response('static/stores_branches.html', '', context_instance=RequestContext(request))

