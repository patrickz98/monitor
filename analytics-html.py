#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import time
import MySQLdb as mdb
from collections import OrderedDict

import conf 
import blacklist
import header
import htmlgenerator

header.main()

con = conf.con
bad = blacklist.bad

list = {}

html = open("aktuell.html", "w+")

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
        
	print "create --> aktuell.html"
    
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
	html.write('			a:visited { text-decoration:none; font-weight:bold; color:#e76e00; }\n')
	html.write('		</style>\n')
	html.write('	</head>\n')

	html.write('	<body>\n')
	html.write('\n')

	html.write('		<h1>' + time.strftime('%H:%M %d.%m.%Y') + '</h1>\n')
	html.write('		<p>Eine Seite zur Weststellung von Medialer Aufmerksamkeit, im Bezug auf Schlagwoerter</p>\n')
	html.write('		<p>Mit Daten von: Spiegel Online, taz.de, Faz, Sueddeuchen, Stern, Zeit, n-tv, Die Welt</p>\n')
	html.write('\n')

	### Search ###
	html.write('		<form name="input" action="search.php" method="get">\n')
	html.write('			<input type="text" name="search" size="40" maxlength="50">\n')
	html.write('			<input type="submit" value="Suchen">\n')
	html.write('		</form>\n')
	html.write('\n')
	
	html.write('		<p style="font-size:65px;"></p>\n')

	for word in list:
		if list[word] >= 8 and word not in bad:
			
			if "\"" in word: word = re.sub(r"\"", "", word)
			
			html.write(('\t\t<p style="font-size:%dpx;">' % int(list[word] * 4.5)) + \
						('<a href="./html/%s.html">' % str(word)) + str(word) + ': ' + str(list[word]) + \
						'</a></p>\n')

			### Html Generierung ####
			htmlgenerator.main(word)
	
	html.write('	</body>\n')
	html.write('</html>\n')
	html.close()
	list = OrderedDict(sorted(list.items(), key=lambda x:x[1]))

main()
mydata()
