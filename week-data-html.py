#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import MySQLdb as mdb

import blacklist
import conf
import htmlgenerator
from mysql import mysqldata

con = conf.con

def week():
	known = []
	### db, (Word, Cluster) ###
	highlight = {}

	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		
		datadb = cur.execute("SHOW TABLES")
		rows = cur.fetchall()
		data = [x['Tables_in_%s' % conf.db] for x in rows if "data" in x['Tables_in_%s' % conf.db]]
				
		for db in data:
			cur.execute("SELECT * FROM %s" % db)
			Words = cur.fetchall()

			cache = {}
			for x in Words:
				cache.update({ int(x["Cluster"]) : x["Word"]  })
			
			highlight.update({ db : (cache[max(cache)], max(cache)) })
				
				
	return highlight

def main():
	weekword = week()

	data = []
	for x in reversed(sorted(weekword)):
#		print  weekword[x], x
		data.append(x)
	
	print "create --> ./week-data.html"

	html = open("week-data.html", "w+")
	
	html.write('<!doctype html>\n')
	html.write('<html>\n')
	html.write('	<head>\n')
	html.write('\n')

	html.write('		<title>Die Woche</title>\n')
	html.write('		<link rel="icon" type="image/x-icon" href="../news.ico" />\n')
	html.write('		<link rel="apple-touch-icon" href="../news.png"/>\n')
	html.write('\n')

	html.write('		<style type="text/css">\n' )
	html.write('			a:link { text-decoration:none; color:#e76e00; }\n')
	html.write('			a:visited { text-decoration:none; color:#e76e00; }\n')
	html.write('		</style>\n')
	html.write('\n')

	html.write('	</head>\n')
	html.write('	<body>\n')

	for x in data:
			html.write('\t\t<h1>%s</h1>\n' % (x[4:][-2:] + "." + x[4:][4:-2] + "." + x[4:][:4]))
			
			html.write('\t\t<p style="color:#e76e00;font-size:%dpx"><a href="%s%s.html">%s: %d</a></p>\n' 
						% (weekword[x][1], conf.htmldir, weekword[x][0], 
						   weekword[x][0], weekword[x][1]))
			
			htmlgenerator.main(weekword[x][0])

	html.write('\t\t<p style="font-size:20px;">&nbsp;</p>\n')
	html.write('	</body>\n')
	html.write('</html>\n')
	
	html.close()

main()
con.close()
