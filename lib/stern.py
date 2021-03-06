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
				if "\\" in title: title = re.sub(r"\\", "", title)
				if "/" in title: title = re.sub(r"/", "", title)

#				if "-" in title: title = re.sub(r"-", " ", title)

# 				if "ß" in title: title = re.sub(r"ß", "ss", title)
# 				if "Ä" in title: title = re.sub(r"Ä", "Ae", title)
# 				if "ä" in title: title = re.sub(r"ä", "ae", title)
# 				if "Ü" in title: title = re.sub(r"Ü", "Ue", title)
# 				if "ü" in title: title = re.sub(r"ü", "ue", title)
# 				if "Ö" in title: title = re.sub(r"Ö", "Oe", title)
# 				if "ö" in title: title = re.sub(r"ö", "oe", title)

				title = regexhtml.main(title)
				link = x[0]

				cache.update({unicodedata.normalize('NFKD', title.decode("utf8")).encode('ascii','ignore') : link})
 				last = title
 	find = cache

	con = conf.con
	with con:

	    cur = con.cursor()

    	    for word in find:

	    	cur.execute("INSERT INTO news%s(Headlines, Newspaper, link) VALUES('%s', '%s', '%s')" % \
	    		(str(time.strftime("%Y%m%d")), str(word), 'Stern', str(find[word])))

		con.commit()
