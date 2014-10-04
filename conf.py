#!/usr/bin/python
import os
import MySQLdb as mdb

import blacklist

bad = blacklist.bad
htmldir = "./html/"
con = mdb.connect('odroid-u3.local', 'monitor', 'test123', 'monitor')