#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time
import re
import MySQLdb as mdb
import operator
from collections import OrderedDict

import blacklist
import conf
from htmlgenerator import graph
from mysql import mysqldata
from mysql import mysqlnews

con = conf.con

def average(word):
	mysql = mysqldata(word)
	cache = 0
	for x in mysql:
		cache += int(mysql[x])
	
	return cache / len(mysql)

def week():
	known = []
	### Word, average, days ###
	highlight = {"Word" : "Word", "average" : 0, "days" : 0}

	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		
		datadb = cur.execute("SHOW TABLES")
		rows = cur.fetchall()
		data = [x['Tables_in_%s' % conf.db] for x in rows if "data" in x['Tables_in_%s' % conf.db]]
		
		cache = 0
		
		for db in data:
			cur.execute("SELECT * FROM %s" % db)
			Words = cur.fetchall()

			for x in Words:
				data = len(mysqldata(x["Word"]))
				
				if data >= cache and x["Word"] not in known:
					aver = average(x["Word"])
								
					if highlight["average"] < aver:
						highlight.update({ "Word" : x["Word"], "average" : aver, "days" : data })
						cache = data

					known.append(x["Word"])

	return highlight

def main():
	print "create -->  ./week-word.html"

	weekword = week()	
	word = weekword["Word"]

	html = open("week-word.html", "w+")


	cache = mysqlnews(word)
	cache2 = sorted(mysqlnews(word), key=operator.itemgetter(2))
	
	html.write('<!doctype html>\n')
	html.write('<html>\n')
	html.write('	<head>\n')
	html.write('\n')

	html.write('		<title>Woche</title>\n')
	html.write('		<link rel="icon" type="image/x-icon" href="./news.ico" />\n')
	html.write('		<link rel="apple-touch-icon" href="./news.png"/>\n')
	html.write('\n')

	html.write('		<script src="./Chart.js"></script>\n')
	html.write('		<style type="text/css">\n' )
	html.write('			a:link { text-decoration:none; color:#000000; }\n')
	html.write('			a:visited { text-decoration:none; color:#e76e00; }\n')
	html.write('\n')

	html.write('		</style>\n')
	html.write('\n')

	html.write('	</head>\n')
	html.write('	<body>\n')
	html.write('		<h1>' + word + '</h1>\n')
	html.write('		<h3>Durchschnittswert von ' + str(weekword["average"]) + " Artikeln an " + str(weekword["days"]) + ' Tagen</h3>\n')

	
	try:
		html.write("\t\t<p>" +  "Artikel Heute mit " + word + ": " + str(mysqldata(word)[time.strftime("%Y%m%d")]) + "</p>\n")
	except:
		html.write("\t\t<p>" +  "Artikel Heute mit " + word + ":" + "</p>\n")
		
	graph(word, html)
		
	html.write("\t\t<h1>" +  "Schlagzeilen Heute: " + "</h1>\n")
	
	for x in cache2:
		if x[2] == time.strftime("%Y%m%d"):
			title = x[0] + " (" + x[1] + ")"
			html.write('		<p style="font-size:19px"><a href="%s" target="_blank">%s</a></p>\n' % (cache[x], title))

	
	html.write("		<p></p>\n")
	html.write("		<h1>" +  "Archiv:" + "</h1>\n")
	html.write("		<p></p>\n")
	
	lastdate = ""
	for x in reversed(cache2):
		if x[2] != time.strftime("%Y%m%d"):
			date = x[2][-2:] + "." + x[2][4:-2] + "." + x[2][:4]
			if lastdate != date:
				html.write("\t\t<h2 id=\'%s\'>%s</h2>\n" % (date, date))
				lastdate = date

			title = x[0] + " (" + x[1] + ")"
			html.write('\t\t<p style="font-size:19px"><a href="%s" target="_blank">%s</a></p>\n' % (cache[x], title))

	html.write('\t\t<p style="font-size:20px;">&nbsp;</p>\n')
	html.write("</body>\n")
	html.write("</html>\n")

	html.close()

main()
con.close()
