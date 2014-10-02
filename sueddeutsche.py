#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import unicodedata
import time
from urllib2 import Request, urlopen, URLError

import conf
import regexhtml

def sueddeutsche():
	request = Request('http://www.sueddeutsche.de/')

	try:
		response = urlopen(request)
		html = response.read()
	except URLError, e:
	    print 'Error:', e

	find = re.findall("<a href=\"(.*?)\".*?<strong>(.*?)</strong>.*?<em>(.*?)</em>.*", html)
	find2 = re.findall("<a href=\"(.*?)\".*?<em>(.*?)</em>.*", html)

	cache = {}
	for x in find:
		title = x[1] + x[2]

		if "\"" in title: title = re.sub(r"\"", "", title)
		if "'" in title: title = re.sub(r"'", "", title)
		if "„" in title: title = re.sub(r"„", "", title)
		if "“" in title: title = re.sub(r"“", "", title)
		if "-" in title: title = re.sub(r"-", " ", title)

		title = regexhtml.main(title)

		cache.update({unicodedata.normalize('NFKD', title.decode("utf8")).encode('ascii','ignore') : x[0]})
	find = cache

 	cache2 = {}
 	for x in find2:
		title = x[1]

		if "\"" in title: title = re.sub(r"\"", "", title)
		if "'" in title: title = re.sub(r"'", "", title)
		if "„" in title: title = re.sub(r"„", "", title)
		if "“" in title: title = re.sub(r"“", "", title)
		if "-" in title: title = re.sub(r"-", " ", title)

		title = regexhtml.main(title)
		cache2.update({unicodedata.normalize('NFKD', title.decode("utf8")).encode('ascii','ignore') : x[0]})
 	find2 = cache2

	bla = []
	
	con = conf.con
	with con:
    
		cur = con.cursor()
		for word in find:	    	        	    			
	    		cur.execute("INSERT INTO news%s(Headlines, Newspaper, link) VALUES('%s', '%s', '%s')" % \
	    			(str(time.strftime("%Y%m%d")), str(word), 'sueddeutsche', str(find[word])))
			bla.append(word)
	
		for word in find2:
#			if  not in bla and len(word) > 10 and "SZ" not in word and "Bundesliga" not in word and "Kalender" not in word and "ueddeutsche" not in word:
			
			cur.execute("INSERT INTO news%s(Headlines, Newspaper, link) VALUES('%s', '%s', '%s')" % \
   				(str(time.strftime("%Y%m%d")), str(word), 'sueddeutsche', str(find2[word])))
	
		con.commit()
