#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import MySQLdb as mdb

import blacklist

bad = blacklist.bad
exception = blacklist.exception

host = "odroid-u3.local"
dbuser = "monitor"
dbpass = "test123"
db = "monitor"
con = mdb.connect(host, dbuser, dbpass, db)

#con = mdb.connect('192.168.0.28', 'monitor', 'test123', 'monitor')
