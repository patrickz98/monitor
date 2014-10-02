#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import unicodedata
import time
from urllib2 import Request, urlopen, URLError

import conf
import regexhtml

def tagesspiegel():
	request = Request('http://www.tagesspiegel.de/schlagzeilen/')

	try:
		response = urlopen(request)
		html = response.read()
	except URLError, e:
	    print 'Error:', e

	find = re.findall('<a title=\"(.*?)\".*?href=\"(.*?)\"', html)
	bla = []
	
	cache = {}
	for x in find:
		title = x[0]
		link = 'http://www.tagesspiegel.de/schlagzeilen' + x[1]
		if len(title) > 15 and title not in bla \
			and "Tagesspiegel" not in title \
			and "Mediadaten" not in title \
			and "Sie haben Mut zur Uni" not in title:

			if "\"" in title: title = re.sub(r"\"", "", title)
			if "'" in title: title = re.sub(r"'", "", title)
			if "„" in title: title = re.sub(r"„", "", title)
			if "“" in title: title = re.sub(r"“", "", title)
			if "-" in title: title = re.sub(r"-", " ", title)

			title = regexhtml.main(title)

			cache.update({unicodedata.normalize('NFKD', title.decode("utf8")).encode('ascii','ignore') : link})
 	find = cache

	con = conf.con
	with con:
    
	    cur = con.cursor()
	    
    	    for word in find:
			
	    	cur.execute("INSERT INTO news%s(Headlines, Newspaper, link) VALUES('%s', '%s', '%s')" % \
	    		(str(time.strftime("%Y%m%d")), str(word), 'tagesspiegel', str(find[word])))

		con.commit()