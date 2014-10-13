#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import time
import MySQLdb as mdb
from collections import OrderedDict

import conf 
import blacklist
#import header
import htmlgenerator

#header.main()

con = conf.con
bad = blacklist.bad

list = {}

html = open("aktuell-unsort.html", "w+")

def mysql():
	Headlines = {}
	with con:

	    	cur = con.cursor(mdb.cursors.DictCursor)
	    	cur.execute("SELECT * FROM news%s" % time.strftime("%Y%m%d"))

	    	rows = cur.fetchall()

	    	for row in rows:
        		Headlines.update({row["Headlines"] : row["Newspaper"]})

			con.commit()

	return Headlines

data = mysql()

def find(word):
	global data
	count = 0
	for a in data:
		if word in a:
			count = count + 1
	return count

def mydata():
	with con:
    
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS data%s" % str(time.strftime("%Y%m%d")))
    
		cur.execute("CREATE TABLE data%s(Word VARCHAR(35), Cluster VARCHAR(4))" % \
    			str(time.strftime("%Y%m%d")))
		
		for Cluster in list:
			cur.execute("INSERT INTO data%s(Word, Cluster) VALUES('%s', '%s')" % \
				(str(time.strftime("%Y%m%d")), str(Cluster), str(list[Cluster])))
		
		con.commit()
	con.close()

def main():
	global list
	global data
        
	for b in data:
		for c in b.split():
			if ":" in c: c = c[:-1]
			if str(c) not in bad and c != "" and len(str(c)) > 3 or str(c) in blacklist.exception:
				if find(c) > 6:
					list.update({c:find(c)})

	html.write('<!doctype html>\n')
	html.write('<html>\n')
	html.write('	<head>\n')
	html.write('		<title>Monitor</title>\n')
	html.write('		<link rel="icon" type="image/x-icon" href="news.ico" />\n')
	html.write('		<link rel="apple-touch-icon" href="news.png"/>\n')
	html.write('\n')
	html.write('		<style type="text/css">\n' )
	html.write('			a:link { text-decoration:none; font-weight:bold; color:#000000; }\n')
	html.write('			a:visited { text-decoration:none; font-weight:bold; color:#0063b0; }\n')
	html.write('		</style>\n')
	html.write('	</head>\n')
	html.write('	<body>\n')
	html.write('\n')
	html.write('		<h1>' 'Monitor: ' + time.strftime('%H:%M %d.%m.%Y') + '</h1>\n')
	html.write('\n')
	
	### Button to Normal site ###
	html.write('		<input type=button\n')
	html.write('			onClick="parent.location=\'aktuell-sort.html\'"\n')
	html.write('			value="Normal"\n')
	html.write('			style="height:25px; width:80px">\n')

	### Button to Sort site ###
	html.write('		<input type=button\n')
	html.write('			onClick="parent.location=\'aktuell-sort.html\'"\n')
	html.write('			value="Unsort"\n')
	html.write('			style="height:25px; width:80px">\n')

	
	html.write('		<p style="font-size:65px;"></p>\n')
		
	for word in list:
		if list[word] >= 8 and word not in bad:
			
			if "\"" in word: word = re.sub(r"\"", "", word)
			
			html.write(('\t\t<p style="font-size:%dpx;display:inline"> ' % int(list[word] * 2)) + \
						('<a href="./html/%s.html">' % str(word)) + str(word) + ' ' + str(list[word]) + \
						';  ' + '</a></p>\n')

			### Html Generierung ####
			htmlgenerator.main(word)
	
	html.write('	</body>\n')
	html.write('</html>\n')
	html.close()
	list = OrderedDict(sorted(list.items(), key=lambda x:x[1]))
	
# 	print time.strftime("%H:%M %d.%m.%Y")
# 	print 
# 	
#  	for l in reversed(list):
#  		if list[l] > 6 and l not in bad:
#  			print l + ": " + str(list[l])

main()
mydata()