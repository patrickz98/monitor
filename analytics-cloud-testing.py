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

	txt = open("cloud.txt", "w")

	for headline in news:
		cluster_string = []
		for word in cluster:
			if word in headline:
				cluster_string.append(word)

		if len(cluster_string) >= 3:
			for fund in cluster_string:
				sys.stdout.write(fund + " ")

			sys.stdout.write("\n")

			txt.write(" ".join(cluster_string) + "\n")
			txt.write(headline + "\n\n")
			txt.flush()


	txt.close()

main()
