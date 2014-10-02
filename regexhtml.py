#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import encodings

def main(news):
	b = news
	if "&Auml;" in b: b = re.sub(r"&Auml;", "Ae", b)
	if "&auml;" in b: b = re.sub(r"&auml;", "ae", b)
	if "&Ouml;" in b: b = re.sub(r"&Ouml;", "Oe", b)
	if "&ouml;" in b: b = re.sub(r"&ouml;", "oe", b)

	if "&Uuml;" in b: b = re.sub(r"&Uuml;", "Ue", b)
	if "&uuml;" in b: b = re.sub(r"&uuml;", "ue", b)
	if "&szlig;" in b: b = re.sub(r"&szlig;", "ß", b)

	if "&quot;" in b: b = re.sub(r"&quot;", '"', b)
	if "&" in b and ";" in b: b = re.sub("&(#?)(\d{1,5}|\w{1,8});", "", b)
	return b
