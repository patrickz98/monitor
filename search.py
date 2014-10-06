#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import MySQLdb as mdb

import conf

con = conf.con

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

search = raw_input("Suche: ")
title = mysqlnews(search)
print "Artikel mit " + search + ": " + str(len(title))
print
for x in title:
	date = x[2][-2:] + "." + x[2][4:-2] + "." + x[2][:4]
	print x[0], "(" + x[1] + ")", "(" + date+ ")"