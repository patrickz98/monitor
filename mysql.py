#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as mdb

import conf

con = conf.con

def get_news(date):
	Headlines = {}

	with con:

		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute("SELECT * FROM news%s" % str(date))

		rows = cur.fetchall()

		for row in rows:
			Headlines.update( {row["Headlines"] : row["Newspaper"]} )

		con.commit()

	return Headlines

def get_news_data(date):
	Headlines = {}
	with con:

	    	cur = con.cursor(mdb.cursors.DictCursor)
	    	cur.execute("SELECT * FROM data%s" % str(date))

	    	rows = cur.fetchall()

	    	for row in rows:
        		Headlines.update({row["Word"] : row["Cluster"]})

			con.commit()

	return Headlines

def mysqlnews(search):
	find = {}

	with con:
		cur = con.cursor(mdb.cursors.DictCursor)

		datadb = cur.execute("SHOW TABLES")
		rows = cur.fetchall()
		data = [x['Tables_in_%s' % conf.db] for x in rows if "news" in x['Tables_in_%s' % conf.db]]

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
		data = [x['Tables_in_%s' % conf.db] for x in rows if "data" in x['Tables_in_%s' % conf.db]]

		for db in data:
			cur.execute("SELECT * FROM %s" % db)
			Cluster = cur.fetchall()

			for Word in Cluster:
				if search in Word["Word"]:
					find.update({ db[4:] : Word["Cluster"] })

	return find
