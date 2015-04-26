#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time

while(True):
	os.popen("python analytics.py").readlines()
	time.sleep(3600 * 2)
#	time.sleep(21600)
