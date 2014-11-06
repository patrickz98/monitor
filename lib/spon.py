#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import unicodedata
import time
from urllib2 import Request, urlopen, URLError

import conf
import regexhtml

def spon():
	request = Request('http://www.spiegel.de/schlagzeilen/')

	try:
		response = urlopen(request)
		html = response.read().decode('latin1')
	except URLError, e:
	    print 'Error:', e
	
	find = re.findall('<a href=\"(.*?)\".*?title="(.*?)\">', html)
			
	cache = {}
	for x in find:
		title = x[1].encode('utf-8')

		if "\"" in title: title = re.sub(r"\"", "", title)
		if "'" in title: title = re.sub(r"'", "", title)
		if "„" in title: title = re.sub(r"„", "", title)
		if "“" in title: title = re.sub(r"“", "", title)
		if "\\" in title: title = re.sub(r"\\", "", title)
		if "/" in title: title = re.sub(r"/", "", title)

#		if "-" in title: title = re.sub(r"-", " ", title)	

# 		if "ß" in title: title = re.sub(r"ß", "ss", title)
# 		if "Ä" in title: title = re.sub(r"Ä", "Ae", title)
# 		if "ä" in title: title = re.sub(r"ä", "ae", title)
# 		if "Ü" in title: title = re.sub(r"Ü", "Ue", title)
# 		if "ü" in title: title = re.sub(r"ü", "ue", title)
# 		if "Ö" in title: title = re.sub(r"Ö", "Oe", title)
# 		if "ö" in title: title = re.sub(r"ö", "oe", title)
		
		title = regexhtml.main(title)

		cache.update({unicodedata.normalize('NFKD', title.decode("utf8")).encode('utf8','ignore') : x[0]})
 	find = cache
	
	con = conf.con
	with con:
    
	    cur = con.cursor()
	    
    	    for word in find:
    	    	if not "Newsletter" in word and not "Anzeige" in word and not "class" in word:
    	    		link = "http://www.spiegel.de" + find[word]
			cur.execute("INSERT INTO news%s(Headlines, Newspaper, link) VALUES('%s', '%s', '%s')" % \
				(str(time.strftime("%Y%m%d")), str(word), 'Spiegel Online', str(link)))
		con.commit()