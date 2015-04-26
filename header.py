#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import sys

import conf

from lib import tagesspiegel
from lib import welt
from lib import zeit
from lib import sueddeutsche
from lib import stern
from lib import spon
from lib import faz
from lib import ntv
from lib import taz
from lib import handelsblatt
from lib import focus


def main():
	con = conf.con
	with con:
		cur = con.cursor()

		cur.execute("DROP TABLE IF EXISTS news%s" % str(time.strftime("%Y%m%d")))

		cur.execute("CREATE TABLE news%s(Headlines VARCHAR(300), Newspaper VARCHAR(20), link VARCHAR(400))" % \
    		str(time.strftime("%Y%m%d")))

	sys.stdout.write("%-18s" % "\rtagesspiegel")
	sys.stdout.flush()
	try:
		tagesspiegel.tagesspiegel()
	except:
		sys.stderr.write("\033[91mTagesspiegel Offline\033[0m\n")


	sys.stdout.write("%-18s" % "\rWelt")
	sys.stdout.flush()
	try:
		welt.welt()
	except:
		sys.stderr.write("\033[91mWelt Offline\033[0m\n")


	sys.stdout.write("%-18s" % "\rZeit Online")
	sys.stdout.flush()
	try:
		zeit.zeit()
	except:
		sys.stderr.write("\033[91mZeit Online Offline\033[0m\n")


	sys.stdout.write("%-18s" % "\rSueddeutsche")
	sys.stdout.flush()
	try:
		sueddeutsche.sueddeutsche()
	except:
		sys.stderr.write("\033[91mSueddeutsche Offline\033[0m\n")

	sys.stdout.write("%-18s" % "\rStern")
	sys.stdout.flush()
	try:
		stern.stern()
	except:
		sys.stderr.write("\033[91mStern Offline\033[0m\n")

	sys.stdout.write("%-18s" % "\rSiegel Online")
	sys.stdout.flush()
	try:
		spon.spon()
	except:
		sys.stderr.write("\033[91mSiegel Online Offline\033[0m\n")

	sys.stdout.write("%-18s" % "\rFAZ")
	sys.stdout.flush()
	try:
		faz.faz()
	except:
		sys.stderr.write("\033[91mFaz Offline\033[0m\n")

	sys.stdout.write("%-18s" % "\rntv")
	sys.stdout.flush()
	try:
		ntv.ntv()
	except:
		sys.stderr.write("\033[91mn-tv Offline\033[0m\n")

	sys.stdout.write("%-18s" % "\rtaz.de")
	sys.stdout.flush()
	try:
		taz.taz()
	except:
		sys.stderr.write("\033[91mtaz.de Offline\033[0m\n")

	sys.stdout.write("%-18s" % "\rHandelsblatt")
	sys.stdout.flush()
	try:
		handelsblatt.handelsblatt()
	except:
	        sys.stderr.write("\033[91mHandelsblatt Offline\033[0m\n")

	sys.stdout.write("%-18s" % "\rFocus\n")
	sys.stdout.flush()
	try:
		focus.focus()
	except:
	        sys.stderr.write("\033[91mFocus Offline\033[0m\n")
