# -*- coding: utf-8 -*-

import re

ingredientexpr = re.compile(r"<span itemprop=\"ingredient\"[^>]*><[^>]*www\.povarenok\.ru/recipes/ingredient/(\d+)[^>]*>[^>]*>([^<]+)[^>]*>[^>]*>[^>]*>([^<]+)<")

remscriptsexpr = re.compile(r"<(S|s)cript[^>]*></(S|s)cript>")

timeexpr = re.compile(r"<time datetime=\"([^\"]+)\"[^>]*>([^<]+)<")

platesexpr = re.compile(u"<strong>Количество порций:</strong>([^<]+)<")

summaryexpr = re.compile(r"<span itemprop=\"summary\">([^<]+)<")

titleexpr = re.compile(r"<h1><[^>]*>([^<]+)<")

data = remscriptsexpr.sub("index.html", data)

title = titleexpr.search(data).group(1).strip()
print u"title = {}".format(title)

summary = summaryexpr.search(data).group(1).strip()
print u"summary = {}".format(summary)

timeneeded = timeexpr.search(data)
if timeneeded is None:
	timeneeded = ("N/A", "?")
else:
	timeneeded = (timeneeded.group(1), timeneeded.group(2).strip())
print u"time = {}; value = {}".format(timeneeded[0], timeneeded[1])

plates = platesexpr.search(data)
if plates is None:
	plates = "?"
else:
	plates = plates.group(1).strip()
print u"plates = {}".format(plates)

ingredients = ingredientexpr.findall(data)
for ing in ingredients:
	print u"id = {}; name = {}; amount = {}".format(ing[0], ing[1], ing[2])
