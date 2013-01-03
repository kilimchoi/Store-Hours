from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
def index(request):
    return render_to_response('static/index.html', '', context_instance=RequestContext(request))

def store_display(request):
	return render_to_response('static/specific_store_display.html', '', context_instance=RequestContext(request))

def branches_display(request):
	return render_to_response('static/stores_branches.html', '', context_instance=RequestContext(request))

