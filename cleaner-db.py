#!/usr/bin/python
import os
import MySQLdb as mdb
import time

import blacklist
import conf

def main():
	con = conf.con
	bad = blacklist.bad

	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		
		datadb = cur.execute("SHOW TABLES")
		rows = cur.fetchall()
		data = [x['Tables_in_%s' % conf.db] for x in rows]
		
		for x in data:
			if int(time.strftime("%Y%m%d")) - 14 > int(x[4:]):
				print "Delt -->", x
				cur.execute("DROP TABLE %s" % x)

	
	con.commit()
	con.close()
main()