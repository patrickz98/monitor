#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import encodings

def main(text):
	title = text
	if "&Auml;" in title: title = re.sub(r"&Auml;", "Ae", title)
	if "&auml;" in title: title = re.sub(r"&auml;", "ae", title)
	if "&Ouml;" in title: title = re.sub(r"&Ouml;", "Oe", title)
	if "&ouml;" in title: title = re.sub(r"&ouml;", "oe", title)

	if "&Uuml;" in title: title = re.sub(r"&Uuml;", "Ue", title)
	if "&uuml;" in title: title = re.sub(r"&uuml;", "ue", title)
	if "&szlig;" in title: title = re.sub(r"&szlig;", "ss", title)

	if "&quot;" in title: title = re.sub(r"&quot;", '"', title)
	
	title = re.sub("&(#?)(\d{1,5}|\w{1,8});", "", title)
		
	return title