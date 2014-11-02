#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import unicodedata
import time
from urllib2 import Request, urlopen, URLError

import conf
import regexhtml

def taz():
	request = Request('http://www.taz.de/')

	try:
		response = urlopen(request)
		html = response.read()
	except URLError, e:
	    print 'Error:', e

	find = re.findall("<a href=\"(.*?)\".*?<h4>(.*?)</h4>.*?<h3>(.*?)</h3>", html)
	
	cache = {}
	for x in find:
		title = x[1] + ": " + x[2]

		if "\"" in title: title = re.sub(r"\"", "", title)
		if "'" in title: title = re.sub(r"'", "", title)
		if "„" in title: title = re.sub(r"„", "", title)
		if "“" in title: title = re.sub(r"“", "", title)
#		if "-" in title: title = re.sub(r"-", " ", title)

# 		if "ß" in title: title = re.sub(r"ß", "ss", title)
# 		if "Ä" in title: title = re.sub(r"Ä", "Ae", title)
# 		if "ä" in title: title = re.sub(r"ä", "ae", title)
# 		if "Ü" in title: title = re.sub(r"Ü", "Ue", title)
# 		if "ü" in title: title = re.sub(r"ü", "ue", title)
# 		if "Ö" in title: title = re.sub(r"Ö", "Oe", title)
# 		if "ö" in title: title = re.sub(r"ö", "oe", title)

		title = regexhtml.main(title)
		link = 'http://www.taz.de' + x[0]
		
		cache.update({unicodedata.normalize('NFKD', title.decode("utf8")).encode('utf8','ignore') : link})
 	find = cache
	
	con = conf.con
	with con:
    
	    cur = con.cursor()
	    
    	    for word in find:
	    	cur.execute("INSERT INTO news%s(Headlines, Newspaper, link) VALUES('%s', '%s', '%s')" % \
	    		(str(time.strftime("%Y%m%d")), str(word), 'taz', str(find[word])))

		con.commit()