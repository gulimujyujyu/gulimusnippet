#@name: wallpaper_from_smashing.py
#@author: gulimujyujyu
#@date: 28-11-2011
#@dependency: BeautifulSoup
#@usage: wallpaper_from_smashing.py 11-2011 [1280*768]

#!/usr/local/bin/python

from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
import urllib2
import time
import sys
import re
import os

#globals
smashing_url = "http://www.smashingmagazine.com"
months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
month_names = ["january","february","march","april","may","june","july","august","september","october","november","december"]

def usage():
	print '''======================================================================================================
Usage:\twallpaper_from_smashing.py -t [month]-[year] -s [width]*[height] -d filename -h
======================================================================================================
e.g. For help, type:\n\twallpaper_from_smashing.py -h
     For normal use, type:\n\twallpaper_from_smashing.py -t 11-2011 -s 1280*800
     For debug use, first get the html using curl, then type:\n\twallpaper_from_smashing.py -s 1280*800 -d aaa.html
======================================================================================================'''

def process_url(url,param,debug=False):
	if debug is False:
		hdl = urllib2.urlopen(url)
		content = hdl.read()
		hdl.close()
	else:
		hdl = open(url)
		content = hdl.read()
		hdl.close()
	
	soup = BeautifulSoup(content)
	tmp = soup.findAll(name='a')
	
	target_regexp = '^\s+%d&times;%d+\s+$' % (param['width'],param['height'])
	print target_regexp
	if not os.path.exists(month_names[param['month']-1]):
		os.mkdir(month_names[param['month']-1])
	
	for one_a in tmp:
		if re.match(target_regexp,one_a.contents[0]) and one_a['href']:
			filename = one_a['href'].split('/')[-1]
			print 'Downloading %s' % filename
			time.sleep(3)
			print 'Start at %s' % time.asctime()
			try:
				webhdl = urllib2.urlopen(one_a['href'])
				content = webhdl.read()
				webhdl.close()
				
				filepath = '%s/%s' % (month_names[param['month']-1],filename)
				fhdl = open(filepath,"wb")
				fhdl.write(content)
				fhdl.close()
			except urllib2.HTTPError, e:
				print e.code;
			print 'End at %s' % time.asctime()
	
	#print soup.prettify()

print sys.argv
if len(sys.argv) < 2:
	usage()
	sys.exit(0)
	
def parse_argv(argv):
	
	pattern_year_month = '^(\d{2})-(\d{4})$'
	pattern_size = '^(\d+)\*(\d+)$'
	is_debug = False
	url = ""
	year = 2011
	month = 12
	height = 768
	width = 1024
	
	if(len(argv)) < 1:
		usage()
		sys.exit(1)

	for i in range(1,len(argv)):
		ins = argv[i];
		
		if ins == "-t":
			#try different ways of url
			tmp = re.match(pattern_year_month, argv[i+1])

			#valid year and month
			if len(tmp.group(0)) <= 1:
				usage()
				sys.exit(0)

			#print tmp.group(0) #debug

			year = int(tmp.group(2))
			month = int(tmp.group(1))

			#valid year and month
			if year < 0 or year > 9999:
				usage()
				sys.exit(0)

			if month < 1 or month > 12:
				usage()
				sys.exit(0)
		
			#whether it is lunar year
			if (year%400 == 0 and year%100 != 0) or (year%4 == 0 and year%100 != 0):
				months[1] = 29;
			else:
				months[1] = 28;
		elif ins == "-d":
			print "DEBUG MODE ON..."
			is_debug = True
			url = argv[i+1]
		elif ins == "-s":
			#try different ways of url
			tmp = re.match(pattern_size, argv[i+1])

			#valid year and month
			if len(tmp.group(0)) <= 1:
				usage()
				sys.exit(0)

			print tmp.group(0)

			height = int(tmp.group(2))
			width = int(tmp.group(1))

			#valid year and month
			if height < 0 or height > 9999:
				usage()
				sys.exit(0)

			if width < 0 or width > 9999:
				usage()
				sys.exit(0)
		elif ins == '-h':
			usage()
			sys.exit(1)
		else:
			continue
			
	return {"year": year, "month":month, "height":height, "width":width, "is_debug":is_debug, "url":url}

def main():
	result = parse_argv(sys.argv)
	year = result["year"]
	month = result["month"]
	height = result["height"]
	width = result["width"]
	is_debug = result["is_debug"]
	
	if is_debug:
		url = result["url"]
		print url
		try: 
			process_url(url,result,is_debug)
		except urllib2.HTTPError, e:
			print e.code;
	else:
		#first trial
		url = smashing_url + \
			"/%4d/%2d/%2d/desktop-wallpaper-calendar-%s-2011/" % (year,month-1,months[month-2],month_names[month-1])
		print url
		try: 
			process_url(url,result,is_debug)
		except urllib2.HTTPError, e:
			print e.code;
			
		#second trial
		url = smashing_url + \
			"/%4d/%2d/%2d/free-desktop-wallpaper-calendar-%s-2011/" % (year,month-1,months[month-2],month_names[month-1])	
		url = smashing_wallpaper_url
		print url
		try: 
			process_url(url,result,is_debug)
		except urllib2.HTTPError, e:
			print e.code;

	
if __name__ == "__main__":
	main()
#print content


