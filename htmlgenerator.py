#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time
import re
import MySQLdb as mdb
from collections import OrderedDict
import operator

import conf

htmldir = conf.htmldir

con = conf.con
bad = conf.bad

def mysqlnews(search):
	find = {}

	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		
		datadb = cur.execute("SHOW TABLES")
		rows = cur.fetchall()
		data = [x['Tables_in_monitor'] for x in rows if "news" in x['Tables_in_monitor']]
		
		for db in data:
			cur.execute("SELECT * FROM %s" % db)
			titles = cur.fetchall()
			
			for title in titles:
				if search in title["Headlines"]:
					find.update({ (title["Headlines"], title["Newspaper"], db[4:]) : title["link"] })

	return find
	
def mysqldata(search):
	find = {}

	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		
		datadb = cur.execute("SHOW TABLES")
		rows = cur.fetchall()
		data = [x['Tables_in_monitor'] for x in rows if "data" in x['Tables_in_monitor']]
		
		for db in data:
			cur.execute("SELECT * FROM %s" % db)
			Cluster = cur.fetchall()
			
			for Word in Cluster:
				if search in Word["Word"]:
					find.update({ db[4:] : Word["Cluster"] })

	return find

#print mysqldata('Hongkong')

def graph(word, html):
	
	size = mysqldata(word)
	sort = sorted(size)
		
	if len(size) >= 3:
	
		html.write('		<div style="width:60%">\n')
		html.write('			<div>\n')
		html.write('				<canvas id="%s" height="450" width="600"></canvas>\n' % word)
		html.write('			</div>\n')
		html.write('		</div>\n')
		html.write('\n')
		
		html.write( '		<script>\n' )	
		html.write( '			var randomScalingFactor = function(){ return Math.round(Math.random()*100)};\n')
		html.write( '			var lineChartData%s = {\n' % word )
		html.write( '				labels : %s,\n' % [x[-2:] + "." + x[4:-2] + "." + x[:4] for x in sort])
		html.write( '				datasets : [\n' )
		html.write( '					{\n' )
		html.write( '						label: "%s",\n' % word )
		html.write( '						fillColor : "rgba(151,187,205,0.2)",\n' )
		html.write( '						strokeColor : "rgba(151,187,205,1)",\n' )
		html.write( '						pointColor : "rgba(151,187,205,1)",\n' )
		html.write( '						pointStrokeColor : "#fff",\n' )
		html.write( '						pointHighlightFill : "#fff",\n' )
		html.write( '						pointHighlightStroke : "rgba(151,187,205,1)",\n' )
		html.write( '						data : %s\n' % ''.join(str([size[x] for x in sort])) )
		html.write( '					}\n' )
		html.write( '				]\n' )
		html.write( '			}\n' )
		html.write( '\n' )
		html.write( '			window.onload = function(){\n')
		html.write( '				var ctx%s = document.getElementById("%s").getContext("2d");\n' % (word, word) )
		html.write( '				window.myLine%s = new Chart(ctx%s).Line(lineChartData%s, {\n' % (word, word, word) )
		html.write( '				responsive: true, animation: false });\n' )
		html.write( '			}\n' )
		html.write( '		</script>\n' )


def main(search):
	try:
		os.mkdir(htmldir)
	except OSError:
		pass

	html = open(htmldir + search + ".html", "w+")
	
	cache = mysqlnews(search)
# 	cache2 = sorted(cache, key=operator.itemgetter(2))
# 	cache3 = {}
# 	
# 	for x in cache2:
# 		cache3.update({ x : cache[x] })
# 	
# 	cache = cache3
	
	html.write('<!doctype html>\n')
	html.write('<html>\n')
	html.write('	<head>\n')
	html.write('\n')

	html.write('		<title>%s</title>\n' % search)
	html.write('		<link rel="icon" type="image/x-icon" href="../news.ico" />\n')
	html.write('		<link rel="apple-touch-icon" href="../news.png"/>\n')
	html.write('\n')

	html.write('		<script src="../Chart.js"></script>\n')
	html.write('		<style type="text/css">\n' )
	html.write('			a:link { text-decoration:none; color:#000000; }\n')
	html.write('			a:visited { text-decoration:none; color:#0063b0; }\n')
	html.write('\n')

	html.write('		</style>\n')
	html.write('\n')

	html.write('	</head>\n')
	html.write('	<body>\n')
	html.write('		<h1>' + search + '</h1>\n')
	
	try:
		html.write("<p>" +  "Artikel Heute mit " + search + ": " + str(mysqldata(search)[time.strftime("%Y%m%d")]) + "</p>\n")
	except:
		html.write("<p>" +  "Artikel Heute mit " + search + ":" + "</p>\n")
	
	html.write("<p></p>\n")
		
	graph(search, html)
		
	html.write("		<h2>" +  "Schlagzeilen Heute:" + "</h2>\n")
	html.write("		<p></p>\n")
	
	for x in cache:
		if x[2] == time.strftime("%Y%m%d"):
			title = x[0] + " (" + x[1] + ")" + " (" + x[2][-2:] + "." + x[2][4:-2] + "." + x[2][:4] + ")"
#			print title
			html.write('		<p style="font-size:18px;"><a href="%s" target="_blank">%s</a></p>\n' % (cache[x], title))
#			html.write('		<p><a href="%s">%s</a></p>\n' % (cache[x], title))

	
	html.write("		<p></p>\n")
	html.write("		<h2>" +  "Archiv:" + "</h2>\n")
	html.write("		<p></p>\n")
	
	for x in cache:
		if x[2] != time.strftime("%Y%m%d"):
			title = x[0] + " (" + x[1] + ")" + " (" + x[2][-2:] + "." + x[2][4:-2] + "." + x[2][:4] + ")"
#			print title
			html.write('		<p style="font-size:18px;"><a href="%s" target="_blank">%s</a></p>\n' % (cache[x], title))
#			html.write('		<p><a href="%s">%s</a></p>\n' % (cache[x], title))
		
	html.write("</body>\n")
	html.write("</html>\n")
		
	html.close()
