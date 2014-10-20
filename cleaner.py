#!/usr/bin/python
import os
import MySQLdb as mdb

import blacklist
import conf

def main():
	con = conf.con
	bad = blacklist.bad

	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		
		datadb = cur.execute("SHOW TABLES")
		rows = cur.fetchall()
		data = [x['Tables_in_%s' % conf.db] for x in rows if "data" in x['Tables_in_%s' % conf.db]]

		for db in data:
			cur.execute("SELECT * FROM %s" % db)
			Words = cur.fetchall()
			
			for Word in Words:
				if Word["Word"] in bad:
					print "clean:", db, "-->", Word["Word"]
					cur.execute("DELETE FROM %s WHERE Word = '%s'" % (db, Word["Word"]))
	
	con.commit()
	con.close()
main()

# DELETE FROM data20141002 WHERE Word = 'Fuball';
# 
# 
#     cur = con.cursor(mdb.cursors.DictCursor)
#     cur.execute("SELECT * FROM Writers")
# 
#     rows = cur.fetchall()
# 
#     for row in rows:
#         print row["Id"], row["Name"]