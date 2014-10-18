#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

import conf
from lib import tagesspiegel, welt, zeit, sueddeutsche, stern, spon, faz, ntv, taz

def main():
	con = conf.con
	with con:
		cur = con.cursor()

		cur.execute("DROP TABLE IF EXISTS news%s" % str(time.strftime("%Y%m%d")))
    
		cur.execute("CREATE TABLE news%s(Headlines VARCHAR(200), Newspaper VARCHAR(20), link VARCHAR(300))" % \
    		str(time.strftime("%Y%m%d")))

	try:
		tagesspiegel.tagesspiegel()
	except:
		print "\033[91mSueddeutsche Offline\033[0m"
		
	try:
		welt.welt()
	except:
		print "\033[91mWelt Offline\033[0m"

	try:
		zeit.zeit()
	except:
		print "\033[91mZeit Offline\033[0m"

	try:
		sueddeutsche.sueddeutsche()
	except:
		print "\033[91mSueddeutsche Offline\033[0m"

	try:
		stern.stern()
	except:
		print "\033[91mStern Offline\033[0m"

	try:
		spon.spon()
	except:
		print "\033[91mSiegel Online Offline\033[0m"

	try:
		faz.faz()
	except:
		print "\033[91mFaz Offline\033[0m"

	try:
		ntv.ntv()
	except:
		print "\033[91mn-tv Offline\033[0m"

	try:
		taz.taz()
	except:
		print "\033[91mtaz.de Offline\033[0m"
