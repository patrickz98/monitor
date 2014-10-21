#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time
import re
import MySQLdb as mdb
from collections import OrderedDict
import operator

import conf
from mysql import mysqldata
from mysql import mysqlnews


htmldir = conf.htmldir

con = conf.con
bad = conf.bad

def graph(word, html):
	
	size = mysqldata(word)
	sort = sorted(size)
		
	if len(size) >= 4:
	
		html.write('		<div style="width:90%">\n')
		html.write('				<canvas id="%s" height="450" width="600"></canvas>\n' % word)
		html.write('		</div>\n')
		html.write('\n')
		
		html.write( '		<script>\n' )	
		html.write( '			var lineChartData%s = {\n' % word )
		html.write( '				labels : %s,\n' % [x[-2:] + "." + x[4:-2] + "." + x[:4] for x in sort])
		html.write( '				datasets : [\n' )
		html.write( '					{\n' )
		html.write( '						label: "%s",\n' % word )
		html.write( '						fillColor : "rgba(231, 110, 0, 0.2)",\n' )
		html.write( '						strokeColor : "rgba(231, 110, 0, 1)",\n' )
		html.write( '						pointColor : "rgba(231, 110, 0, 1)",\n' )
		html.write( '						pointStrokeColor : "#fff",\n' )
		html.write( '						pointHighlightFill : "#fff",\n' )
		html.write( '						pointHighlightStroke : "rgba(231, 110, 0, 1)",\n' )
		html.write( '						data : %s\n' % ''.join(str([size[x] for x in sort])) )
		html.write( '					}\n' )
		html.write( '				]\n' )
		html.write( '			}\n' )
		html.write( '\n' )
		html.write( '			window.onload = function(){\n')
		html.write( '				var ctx%s = document.getElementById("%s").getContext("2d");\n' % (word, word) )
		html.write( '				window.myLine%s = new Chart(ctx%s).Line(lineChartData%s, {\n' % (word, word, word) )
		html.write( '				responsive: true, animation: true });\n' )
		html.write( '			}\n' )
		html.write( '		</script>\n' )


def main(search):
	try:
		os.mkdir(htmldir)
	except OSError:
		pass

	print "create --> " + htmldir + search + ".html"

	html = open(htmldir + search + ".html", "w+")

	cache = mysqlnews(search)
	cache2 = sorted(mysqlnews(search), key=operator.itemgetter(2))
	
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
	html.write('			a:visited { text-decoration:none; color:#e76e00; }\n')
	html.write('\n')

	html.write('		</style>\n')
	html.write('\n')

	html.write('	</head>\n')
	html.write('	<body>\n')
	html.write('		<h1>' + search + '</h1>\n')
	
	try:
		html.write("\t\t<p>" +  "Artikel Heute mit " + search + ": " + str(mysqldata(search)[time.strftime("%Y%m%d")]) + "</p>\n")
	except:
		html.write("\t\t<p>" +  "Artikel Heute mit " + search + ":" + "</p>\n")
		
	graph(search, html)
		
	html.write("\t\t<h1>" +  "Schlagzeilen Heute: " + "</h1>\n")
	
	for x in cache2:
		if x[2] == time.strftime("%Y%m%d"):
			title = x[0] + " (" + x[1] + ")"
			html.write('		<p style="font-size:18px;"><a href="%s" target="_blank">%s</a></p>\n' % (cache[x], title))

	
	html.write("		<p></p>\n")
	html.write("		<h1>" +  "Archiv:" + "</h1>\n")
	html.write("		<p></p>\n")

	lastdate = ""
	for x in reversed(cache2):
		if x[2] != time.strftime("%Y%m%d"):
			date = x[2][-2:] + "." + x[2][4:-2] + "." + x[2][:4]
			if lastdate != date:
				html.write("\t\t<h2 id=\"%s\">%s</h2>\n" % (date, date))
				lastdate = date

			title = x[0] + " (" + x[1] + ")"
			html.write('\t\t<p style="font-size:18px;"><a href="%s" target="_blank">%s</a></p>\n' % (cache[x], title))

	html.write('\t\t<p style="font-size:20px;">&nbsp;</p>\n')		
	html.write("</body>\n")
	html.write("</html>\n")
		
	html.close()
