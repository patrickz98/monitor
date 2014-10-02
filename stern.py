#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import unicodedata
import time
from urllib2 import Request, urlopen, URLError

import conf
import regexhtml

def stern():
	request = Request('http://www.stern.de/news/')

	try:
		response = urlopen(request)
		html = response.read()
	except URLError, e:
	    print 'Error:', e
	
	last = ""	
	find = re.findall('<a href=\"(.*?)\".*?title=\"(.*?)\">', html)

	cache = {}
	for x in find:
		title = x[1]
		if len(title) > 18 and len(title) < 110:
			if last != title:

				if "\"" in title: title = re.sub(r"\"", "", title)
				if "'" in title: title = re.sub(r"'", "", title)
				if "„" in title: title = re.sub(r"„", "", title)
				if "“" in title: title = re.sub(r"“", "", title)
				if "-" in title: title = re.sub(r"-", " ", title)
		
				title = regexhtml.main(title)

				cache.update({unicodedata.normalize('NFKD', title.decode("utf8")).encode('ascii','ignore') : x[0]})
 				last = title
 	find = cache
	
	con = conf.con
	with con:
    
	    cur = con.cursor()
	    
    	    for word in find:
    	    			
	    	cur.execute("INSERT INTO news%s(Headlines, Newspaper, link) VALUES('%s', '%s', '%s')" % \
	    		(str(time.strftime("%Y%m%d")), str(word), 'stern', str(find[word])))

		con.commit()
