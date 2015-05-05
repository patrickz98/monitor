#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import sys

import conf
import mysql

def table_print(Word):
	for x in range(0, 2):
		print " |"

	print " +" + "---> " + Word

def print_connections(Word, cluster_strings):
	tmp = []
	for cluster in cluster_strings:
		cluster = cluster.split(" ")
		if Word in cluster:
			for c in cluster:
				if c not in tmp:
					table_print(c)
					tmp.append(c)

def cluster_analytics(data, cluster_strings):
	set = {}

	for cluster in cluster_strings:
		for x in data:

			if x in cluster:

				if x in set:
					set[x] = set[x] + 1
				else:
					set.update({ x : 1 })

	for x in set:
		print
		print x  + ": " + str(set[x])
		print_connections(x, cluster_strings)

def main():
	news = mysql.get_news(time.strftime("%Y%m%d"))
	cluster = mysql.get_news_data(time.strftime("%Y%m%d"))

	txt = open("cloud.txt", "w")

	end_data = []

	for headline in news:
		cluster_string = []
		for word in cluster:
			if word in headline:
				cluster_string.append(word)

		if len(cluster_string) >= 4:

			# sys.stdout.write(" + ".join(cluster_string) + "\n")

			end_data.append(" ".join(cluster_string))
			txt.write(" ".join(cluster_string) + "\n")
			txt.write(headline + "\n\n")
			txt.flush()


	txt.close()
	cluster_analytics(cluster, end_data)

main()
