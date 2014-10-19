#!/usr/bin/python
# -*- coding: utf-8 -*-
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