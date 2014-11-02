#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import unicodedata
import time
from urllib2 import Request, urlopen, URLError

import conf
import regexhtml

def handelsblatt():
	request = Request('http://www.handelsblatt.com')

	try:
		response = urlopen(request)
		html = response.read()
	except URLError, e:
	    print 'Error:', e

	known = []	
	find = re.findall('<a title=\"(.*?)\".*?href=\"(.*?)\">', html)

	cache = {}
	
	for x in find:
		title = x[0]
		if len(title) > 18 and len(title) < 110 and "Handelsblatt" not in title:
			if title not in known:
				known.append(title)
				
				if "\"" in title: title = re.sub(r"\"", "", title)
				if "'" in title: title = re.sub(r"'", "", title)
				if "„" in title: title = re.sub(r"„", "", title)
				if "“" in title: title = re.sub(r"“", "", title)
#				if "-" in title: title = re.sub(r"-", " ", title)

				if title[:1] == " ": title = title[1:]

# 				if "ß" in title: title = re.sub(r"ß", "ss", title)
# 				if "Ä" in title: title = re.sub(r"Ä", "Ae", title)
# 				if "ä" in title: title = re.sub(r"ä", "ae", title)
# 				if "Ü" in title: title = re.sub(r"Ü", "Ue", title)
# 				if "ü" in title: title = re.sub(r"ü", "ue", title)
# 				if "Ö" in title: title = re.sub(r"Ö", "Oe", title)
# 				if "ö" in title: title = re.sub(r"ö", "oe", title)
		
				title = regexhtml.main(title)
				link = 'http://www.handelsblatt.com' + x[1]

				cache.update({unicodedata.normalize('NFKD', title.decode("utf8")).encode('utf8','ignore') : link})
 	find = cache
	
	con = conf.con
	with con:
    
	    cur = con.cursor()
	    
    	    for word in find:
    	    			
	    	cur.execute("INSERT INTO news%s(Headlines, Newspaper, link) VALUES('%s', '%s', '%s')" % \
	    		(str(time.strftime("%Y%m%d")), str(word), 'Handelsblatt', str(find[word])))

		con.commit()