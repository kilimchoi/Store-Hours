
from django.conf.urls import patterns, include, url
from store_hours.views import index, stores_branches, branches_display, hours_display

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    ('^index/$', index),
    ('^stores_branches/$', stores_branches),
    ('^branches_display/$', branches_display),
    ('^hours_display/(?P<store_branch_name>[\w|\W]+)/(?P<address>[\w|\W]+)$', hours_display),

    # Examples:
    # url(r'^$', 'store_locator.views.home', name='home'),
    # url(r'^store_locator/', include('store_locator.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)