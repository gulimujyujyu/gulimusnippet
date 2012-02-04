#@name: csv2html_cheatsheet.py
#@author: gulimujyujyu
#@date: 01-07-2012
#@dependency: Django
#@usage: csv2html_cheatsheet.py -i [blabla.csv] -o [blabla.html]

#!/usr/local/bin/python

import sys, getopt
import csv
import re
from datetime import datetime
from django.template import Template, Context
from django.conf import settings
from django.utils.encoding import smart_str, smart_unicode

#globals
SETTINGS = {'input':'test.csv', 'output':'test.html', 'template':'template_cheatsheet.html'}

def usage():
  print '''======================================================================================================
Usage:\tcsv2html_cheatsheet.py -i [blabla.csv] -o [blabla.html]
======================================================================================================
e.g. For help, type:\n\tcsv2html_cheatsheet.py -h
     For normal use, type:\n\tcsv2html_cheatsheet.py -i vim.csv -o vim.html

NOTE: This script must be companied with template_cheatsheet.html.
======================================================================================================'''

def process_csv():
	#load csv
	csv_data = csv.reader(open(SETTINGS['input'], 'rb'), delimiter=',')
	data = []
	for row in csv_data:
		#print entry
		data.append({'com':row[0],'des':row[1],'exa':row[2],'mea':row[3]})
		
	print data
	return data

def process_filename():
	re_pattern = "^(\w+)(\.((\d+\.)+\d+))?\.csv$"
	doc_re = re.compile(re_pattern)
	rslt = doc_re.match(SETTINGS['input'])
	doc = {}
	if rslt:
		print rslt.groups()
		doc['title'] = rslt.group(1)
		doc['version'] = rslt.group(3)
	else:
		print 'Not Match.'
		doc['title'] = None
		doc['version'] = None
	print doc
	return doc

def output_to_html(data, doc):
	temp_hdl = open(SETTINGS['template'])
	temp_cnt = temp_hdl.read()
	temp_hdl.close()
	#devide data into two colomns
	data_left = data[::2]
	data_right = data[1::2]
	#print data
	now_time = datetime.now()
	ctime = now_time.strftime("%A, %d. %B %Y %I:%M%p")
	print ctime
	cont = Context({"data_left":data_left,"data_right":data_right,"data":data,"doc":doc,"gene_time":ctime})
	#print temp_cnt
	temp = Template(temp_cnt)
	html_cnt = temp.render(cont)
	#print html_cnt
	html_hdl = open(SETTINGS['output'],'w')
	html_hdl.write(smart_str(html_cnt))
	html_hdl.close()

def main():
	#parse arguments
	try:
		options, argvs = getopt.getopt(sys.argv[1:], 'i:o:') #i,o requires arguments
		print options, argvs
		if len(options) <= 0:
			raise getopt.GetoptError('Wrong arguments')
		#check arguments
		for o,v in options:
			if o == '-i':
				SETTINGS['input'] = v
			elif o == '-o':
				SETTINGS['output'] = v
			elif o == '-h':
				usage()
				sys.exit(2)
			else:
				raise getopt.GetoptError('Wrong arguments')
		#process the csv
		doc = process_filename()
		data = process_csv()
		output_to_html( data, doc)
		
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)

if __name__ == "__main__":
	settings.configure(DEBUG=True, TEMPLATE_DEBUG=True,
      TEMPLATE_DIRS=('.'))
	main()