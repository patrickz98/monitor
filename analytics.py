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

header.main()

dir = conf.dir
con = conf.con
bad = blacklist.bad

list = {}

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
        
	for b in data:
		for c in b.split():
			if ":" in c: c = c[:-1]
			if str(c) not in bad and c != "" and len(str(c)) > 3 or str(c) in blacklist.exception:
				if find(c) > 6:
					list.update({c:find(c)})


	list = OrderedDict(sorted(list.items(), key=lambda x:x[1]))
	
	print time.strftime("%H:%M %d.%m.%Y")
	print 
	
 	for l in reversed(list):
 		if list[l] > 6 and l not in bad:
 			print l + ": " + str(list[l])

main()
mydata()