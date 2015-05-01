#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import time
import MySQLdb as mdb
from collections import OrderedDict
import sys

import conf

con = conf.con
bad = conf.bad
exception = conf.exception
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

def mydata():
	Headlines = {}
	with con:

	    	cur = con.cursor(mdb.cursors.DictCursor)
	    	cur.execute("SELECT * FROM data%s" % time.strftime("%Y%m%d"))

	    	rows = cur.fetchall()

	    	for row in rows:
        		Headlines.update({row["Word"] : row["Cluster"]})

			con.commit()

	return Headlines

news = mysql()
cluster = mydata()

def main():
	global news
	global cluster

	txt = open("cloud.txt", "w")
	time = len(cluster) ** 3 * len(news)
	count = 0

	tmp = []

	for x in cluster:
		for y in cluster:
			for z in cluster:
				for headline in news:
					# check if not doubles/triples
					if x != y and x != z and y != z:

						if x in headline and \
						   y in headline and \
						   z in headline:
							print x + " + " + y + " + " + z
							txt.write(x + " + " + y + " + " + z + "\n")
							txt.write(headline + "\n\n")
							txt.flush()

	txt.close()

main()
