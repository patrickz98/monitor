#!/usr/bin/python
import os
import MySQLdb as mdb

import blacklist
import conf

con = conf.con

def count(word):
	size = 0
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		
		datadb = cur.execute("SHOW TABLES")
		rows = cur.fetchall()
		data = [x['Tables_in_monitor'] for x in rows if "data" in x['Tables_in_monitor']]

		for db in data:
			cur.execute("SELECT * FROM %s" % db)
			Words = cur.fetchall()

			for x in Words:
				if x["Word"] == word:
					size = size + 1
				
	return size

def main():
	bad = blacklist.bad
	raw = []
	average = {}
	finish = []

	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		
		datadb = cur.execute("SHOW TABLES")
		rows = cur.fetchall()
		data = [x['Tables_in_monitor'] for x in rows if "data" in x['Tables_in_monitor']]

		for db in data:
			cur.execute("SELECT * FROM %s" % db)
			Words = cur.fetchall()

			for x in Words:
				raw.append((x["Word"], x["Cluster"], db))
	
	### average data ###
	cache = 0
	for x in raw:
		if x[0] not in finish:
			for y in raw:
				if x[0] == y[0] and count(x[0]) == len(data):
					cache = cache + int(y[1])
					average.update({ y[0] : cache })
			cache = 0		
		finish.append(x[0])
	
	### highest average ###
	big = (0, "Word")
	for x in average:
		if average[x] / count(x) > big[0]:
#			print x, average[x], "-->", average[x] / count(x)
			big = (average[x] / count(x), x)
	
	print "most:", big[1], "-->", big[0]
	
	chart = {}
	for x in raw:
		if x[0] == big[1]:
			print x[2], "-->", x[1]
			chart.update({ x[2] : x[1] })

	html = open("week.html", "w+")

	html.write('<!doctype html>\n')
	html.write('<html>\n')
	html.write('	<head>\n')
	html.write('\n')

	html.write('		<title>%s</title>\n' % big[1])
	html.write('		<link rel="icon" type="image/x-icon" href="./news.ico" />\n')
	html.write('		<link rel="apple-touch-icon" href="./news.png"/>\n')
	html.write('\n')

	html.write('		<script src="./Chart.js"></script>\n')
	html.write('		<style type="text/css">\n' )
	html.write('			a:link { text-decoration:none; color:#000000; }\n')
	html.write('			a:visited { text-decoration:none; color:#0063b0; }\n')
	html.write('\n')

	html.write('		</style>\n')
	html.write('\n')

	html.write('	</head>\n')
	html.write('	<body>\n')

	html.write('		<div style="width:90%">\n')
	html.write('				<canvas id="%s" height="450" width="600"></canvas>\n' % big[1])
	html.write('		</div>\n')
	html.write('\n')
		
	html.write( '		<script>\n' )	
	html.write( '			var lineChartData%s = {\n' % big[1] )
	html.write( '				labels : %s,\n' % [x[-2:] + "." + x[4:-2] + "." + x[:4] for x in sorted(chart)])
	html.write( '				datasets : [\n' )
	html.write( '					{\n' )
	html.write( '						label: "%s",\n' % big[1] )
	html.write( '						fillColor : "rgba(0, 99, 176, 0.1)",\n' )
	html.write( '						strokeColor : "rgba(0, 99, 176, 1)",\n' )
	html.write( '						pointColor : "rgba(0, 99, 176, 1)",\n' )
	html.write( '						pointStrokeColor : "#fff",\n' )
	html.write( '						pointHighlightFill : "#fff",\n' )
	html.write( '						pointHighlightStroke : "rgba(0, 99, 176, 1)",\n' )
	html.write( '						data : %s\n' % ''.join(str([chart[x] for x in sorted(chart)])) )
	html.write( '					}\n' )
	html.write( '				]\n' )
	html.write( '			}\n' )
	html.write( '\n' )
	html.write( '			window.onload = function(){\n')
	html.write( '				var ctx%s = document.getElementById("%s").getContext("2d");\n' % (big[1], big[1]) )
	html.write( '				window.myLine%s = new Chart(ctx%s).Line(lineChartData%s, {\n' % (big[1], big[1], big[1]) )
	html.write( '				responsive: true, animation: true });\n' )
	html.write( '			}\n' )
	html.write( '		</script>\n' )

	html.write("</body>\n")
	html.write("</html>\n")

	print "Fertig"

	html.close()
	con.close()
main()