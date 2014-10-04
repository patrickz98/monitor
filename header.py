#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

import conf
import tagesspiegel, welt, zeit, sueddeutsche, stern, spon, faz

def main():
	con = conf.con
	with con:
		cur = con.cursor()

		cur.execute("DROP TABLE IF EXISTS news%s" % str(time.strftime("%Y%m%d")))
    
		cur.execute("CREATE TABLE news%s(Headlines VARCHAR(200), Newspaper VARCHAR(20), link VARCHAR(300))" % \
    		str(time.strftime("%Y%m%d")))

	tagesspiegel.tagesspiegel()
	welt.welt()
	zeit.zeit()
	sueddeutsche.sueddeutsche()
	stern.stern()
	spon.spon()
	faz.faz()

	con.close()
