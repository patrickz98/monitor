#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import encodings

def main(text):
	title = text
	if "&Auml;" in title: title = re.sub(r"&Auml;", "Ä", title)
	if "&auml;" in title: title = re.sub(r"&auml;", "ä", title)
	if "&Ouml;" in title: title = re.sub(r"&Ouml;", "Ö", title)
	if "&ouml;" in title: title = re.sub(r"&ouml;", "ö", title)

	if "&Uuml;" in title: title = re.sub(r"&Uuml;", "Ü", title)
	if "&uuml;" in title: title = re.sub(r"&uuml;", "ü", title)
	if "&szlig;" in title: title = re.sub(r"&szlig;", "ß", title)

	if "&quot;" in title: title = re.sub(r"&quot;", '"', title)

	title = re.sub("&(#?)(\d{1,5}|\w{1,8});", "", title)

	return title
