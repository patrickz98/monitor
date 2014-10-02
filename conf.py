#!/usr/bin/python
import os
import MySQLdb as mdb

dir =  "./words/"
htmldir = "./html/"
text = [x for x in os.listdir(".") if "news-" in x]
con = mdb.connect('odroid-u3.local', 'monitor', 'test123', 'monitor')