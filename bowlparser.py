import urllib
import urllib2
import string
import sys
from bs4 import BeautifulSoup


url = "http://berkeleybowl.com/"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
hours = soup.head
print hours
