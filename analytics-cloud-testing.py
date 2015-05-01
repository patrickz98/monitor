#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import sys

import conf
import mysql

news = mysql.get_news(time.strftime("%Y%m%d"))
cluster = mysql.get_news_data(time.strftime("%Y%m%d"))

def main():
	global news
	global cluster

	cluster_string = [x for x in cluster]
	cluster_string2 = []
	checked_words  = []
	txt = open("cloud.txt", "w")
	status = True
	count = 0

	for uninportant in range(0, 2):
		for test in cluster_string:
			x = test.split(" ")
			for y in cluster:
				# print test + " " + y
				for headline in news:
					status = True

					if y in x:
						status = False
						continue

					for control in x:
						if y in control:
							status = False
							continue

						if control in y:
							status = False
							continue


					for control in x:
						if control not in headline:
							status = False
							continue

					if y in headline and status != False:
						print test + " " + y
						txt.write(test + " " + y + "\n")
						txt.write(headline + "\n\n")
						txt.flush()

						if test + " " + y not in cluster_string2:
							cluster_string2.append(test + " " + y)

			cluster_string = cluster_string2

	txt.close()

main()
