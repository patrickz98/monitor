#!/usr/bin/python
import os
import MySQLdb as mdb

import blacklist
import conf
from mysql import mysqldata

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
		data = [x['Tables_in_monitor'] for x in rows if "data" in x['Tables_in_monitor']]
		
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
	weekword = week()
	print weekword
	
main()
con.close()
