#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import MySQLdb as mdb

import blacklist
import conf
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

	for x in reversed(sorted(weekword)):
		print  weekword[x], x
	
main()
con.close()
